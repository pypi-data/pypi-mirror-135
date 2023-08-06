import datetime
import gspread
import pandas as pd
import numpy as np
import requests

gc = gspread.oauth()
message_data_sheet = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1IfZlLzzwkC05I6fv-4ZRNFOc7ul7k0qIfeG-bk9j6AA/edit#gid=81738738"
).sheet1

specialist_name = "Tylee Evans Groll"

level_10 = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1Y7cQYW1MJ1HstJVJEADVqKgbI-bOMyv74159jOJQtc4/edit#gid=1480274768"
).sheet1

role_dictionary = {
    "Pod Leads": ["Girls", "No_name"],
    "Snr Specialists": [
        "Morgan",
        "Isela",
        "Caycee",
        "Pat",
        "Sean",
        "Kayla",
        "Molly N",
    ],
    "Jnr Specialists": ["Noela", "Molly C", "Zach"],
    "Setters": [
        "Alex",
        "Amanda",
        "Donnah",
        "Liz",
        "Jelyn",
        "Monica",
        "Rachel",
        "Suleyma",
    ],
}


class FBTracking:
    def __init__(self, sheet, specialist):
        self.sheet = sheet
        self.specialist = specialist

    def getSheetValues(self):
        message_data = self.sheet.get_all_records()
        return message_data

    def emptyDictionary(self):
        messages = self.getSheetValues()
        all_messages = [i for i in messages if (len(i["Conversation"]) > 2)]
        return all_messages

    def dictionaryToDataframe(self):
        messages = self.emptyDictionary()
        dataframe = pd.DataFrame(messages)
        return dataframe

    def groupbyConversation(self):
        df = self.dictionaryToDataframe()
        grouped_df = df.groupby(["Conversation"])["Timestamp (ms)"].max()
        return grouped_df

    def listLastSenders(self):
        df = self.dictionaryToDataframe()
        group = self.groupbyConversation()
        last_sender = []
        for row in group:
            last_sender.append(df.loc[df["Timestamp (ms)"] == row]["Sender"].values[0])
        return last_sender

    def countUnanswered(self):
        senders = self.listLastSenders()
        return len(senders) - senders.count(self.specialist)


class AveragePerConversation:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def getProspectNamesInDictionary(self):
        df = self.dataframe
        name_list = sorted(set(list(df["Conversation"].values)))
        return name_list

    def groupDataframeByTimestamp(self):
        timestamp_df = self.dataframe.groupby(["Conversation", "Timestamp (ms)"])[
            "Timestamp (ms)"
        ].unique()
        return timestamp_df

    def createDictionaryWithProspectNamesAndListOfReplyTimes(self):
        name_list = self.getProspectNamesInDictionary()
        timestamp_df = self.groupDataframeByTimestamp()
        dictionary_of_reply_times = {}
        for name in name_list:
            dictionary_of_reply_times[name] = timestamp_df[name].astype(int).tolist()

        return dictionary_of_reply_times

    def getAverageReplyTimePerConversation(self, name):
        reply_time_dict = self.createDictionaryWithProspectNamesAndListOfReplyTimes()
        reply_times = []
        for index, time in enumerate(reply_time_dict[name]):
            if index + 1 == len(reply_time_dict[name]):
                pass
            else:
                first_message_time = reply_time_dict[name][index]
                next_message_time = reply_time_dict[name][index + 1]
                reply_times.append(next_message_time - first_message_time)
        return np.mean(reply_times)

    def getAverageReplyTimeOfAllConversations(self):
        reply_time_dict = self.createDictionaryWithProspectNamesAndListOfReplyTimes()
        list_of_averages = []
        for name in reply_time_dict:
            avg_time = self.getAverageReplyTimePerConversation(name)
            list_of_averages.append(str(avg_time))

        cleaned_averages = [float(i) for i in list_of_averages if i != "nan"]
        return np.mean(cleaned_averages)

    def convertMstoMinutes(self, ms_measurement):
        return round(ms_measurement / 60000, 2)


class Leaderboard:
    def __init__(self, sheet):
        self.sheet = sheet

    def getWeekTotalFromLevel10(self):
        level_10_data = self.sheet.get_all_records()
        level_10_df = (
            pd.DataFrame(level_10_data)[["Metric Type", "Week Total"]]
            .dropna()
            .set_index("Metric Type")
        )
        return level_10_df

    def getDictionaryOfCellsToCheck(self, role_dictionary):
        cells_to_check = {}
        full_list = list(self.getWeekTotalFromLevel10().index.values)

        for role, person_list in role_dictionary.items():
            metrics = []
            for person in person_list:
                for i in full_list:
                    if person in i:
                        metrics.append(i)
                        cells_to_check[role] = metrics
        return cells_to_check

    def getValueForEachTeamMemberInTheirRole(self):

        df = self.getWeekTotalFromLevel10()
        cells = self.getDictionaryOfCellsToCheck(role_dictionary)

        dep_pep = {}
        for role, person_list in cells.items():
            values_per_department = {}
            for person in person_list:
                values_per_department[person] = int(df.loc[person].values[0])
            dep_pep[role] = values_per_department

        dataframe_with_score_and_role = pd.DataFrame(dep_pep)

        return dataframe_with_score_and_role

    def getSortedTCandSSNumbersForTeamMember(self):

        df = self.getValueForEachTeamMemberInTheirRole()
        columns_for_frame = list(role_dictionary.keys())

        list_of_df = []
        for col in columns_for_frame:
            if col == "Jnr Specialists" or col == "Setters":
                frame = df[df[col].index.str.contains("TC")]
            elif col == "Snr Specialists" or col == "Pod Leads":
                frame = df[df[col].index.str.contains("SS")]

            res = frame[col].dropna().sort_values(ascending=False)
            list_of_df.append(res)

        sorted_dataframe_of_TC_and_SS = pd.concat(list_of_df, axis=1)

        return sorted_dataframe_of_TC_and_SS


headers = {
    "Accept": "application/json",
    "API-Key": "d7459f78d474f09276b4d708d2f2a161",
}


class ScheduleOnce:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def getFullBookingList(self):
        response = requests.request("GET", url=self.url, headers=self.headers)
        booking_list = response.json()["data"]

        return booking_list

    def getTCScheduledorTCBookedYesterday(self):
        from_date = str(datetime.date.today() - datetime.timedelta(1))
        to_date = str(datetime.date.today())
        which_params = input(
            "Do you want TC Scheduled (s) or TC Booked (b). Please enter exactly s or b: "
        ).lower()
        if which_params == "s":
            params = {
                "starting_time.gt": from_date,
                "starting_time.lt": to_date,
            }
        elif which_params == "b":
            params = {"creation_time.gt": from_date, "creation_time.lt": to_date}

        response = requests.request(
            "GET", url=self.url, headers=self.headers, params=params
        )
        booking_list = response.json()["data"]

        return booking_list

    def appendMultipleAPIPagesOfTCScheduledorBooked(self):
        bookings = []

        while True:
            all_bookings = self.getTCScheduledorTCBookedYesterday()
            if len(all_bookings) == 100:
                after_id = all_bookings[-1]["id"]
                url = (
                    "https://api.oncehub.com/v2/bookings?after="
                    + after_id
                    + "&limit=100&expand=booking_page"
                )
                new_bookings = ScheduleOnce(
                    url, headers
                ).getTCScheduledorTCBookedYesterday()
                bookings.append(new_bookings)
            elif len(all_bookings) < 100:
                break

            bookings.append(all_bookings)
            new_bookings = [item for sublist in bookings for item in sublist]

            return new_bookings

    def getBookingDataFromListOfBookings(self):
        bookings = self.appendMultipleAPIPagesOfTCScheduledorBooked()
        booking_data = []

        for booking in bookings:
            page_source_name = {}
            page_source_name["Name"] = booking["form_submission"]["name"]
            page_source_name["Page Name"] = booking["booking_page"]["label"]
            try:
                page_source_name["Source"] = booking["form_submission"][
                    "custom_fields"
                ][0]["value"]
            except:
                page_source_name["Source"] = "Inbound Triage"
            booking_data.append(page_source_name)

        return booking_data

    def getValueCountsFromSourceOfPageName(self):
        booking_data = self.getBookingDataFromListOfBookings()
        df = pd.DataFrame(booking_data)
        grouped_by_source = df.groupby("Page Name")["Source"].value_counts()

        return grouped_by_source
