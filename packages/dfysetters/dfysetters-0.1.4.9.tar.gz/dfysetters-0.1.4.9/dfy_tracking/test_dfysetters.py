import pytest
import gspread
import numpy as np
import pandas as pd
import datetime
from dfysetters import ScheduleOnce
from dfysetters import FBTracking
from dfysetters import AveragePerConversation
from dfysetters import Leaderboard

gc = gspread.oauth()
message_data_sheet = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/10t3QySrlJ207MidVHS1Yh_9BmhGFSmfmasQu_qcCdtU/edit#gid=2050205042"
).sheet1
specialist_name = "Tylee Evans Groll"


@pytest.fixture()
def tracking():
    tracking = FBTracking(message_data_sheet, specialist_name)
    return tracking


@pytest.fixture()
def averages():
    df = FBTracking(message_data_sheet, specialist_name).dictionaryToDataframe()
    averages = AveragePerConversation(df)
    return averages


class TestFBTracking:
    def test_canReturnListFromSheet(self, tracking):
        messages = tracking.getSheetValues()
        assert isinstance(messages, list)

    def test_listOfDictionariesHasCorrectKeys(self, tracking):
        messages = tracking.getSheetValues()
        output_keys = messages[0].keys()
        correct_keys = ["Conversation", "Sender", "Timestamp (ms)"]
        assert all(item in output_keys for item in correct_keys)

    def test_canEmptyListOfBadDictionaryEntries(self, tracking):
        all_messages = tracking.emptyDictionary()
        assert 0 not in [len(i["Conversation"]) for i in all_messages]

    def test_canCreateDataframeFromDictionary(self, tracking):
        dataframe = tracking.dictionaryToDataframe()
        assert isinstance(dataframe, pd.DataFrame)

    def test_canGroupBasedOnConversation(self, tracking):
        grouped_data = tracking.groupbyConversation()
        assert 1610000000000 < np.mean(grouped_data)

    def test_returnSenderOfHighestTimestamp(self, tracking):
        last_sender_list = tracking.listLastSenders()
        assert specialist_name in last_sender_list

    def test_countingHowManyUnanswered(self, tracking):
        unanswered = tracking.countUnanswered()
        assert isinstance(unanswered, int)


class TestAveragePerConversation:
    def test_getProspectNamesInDictionary(self, averages, tracking):
        name_list = averages.getProspectNamesInDictionary()
        df = tracking.dictionaryToDataframe()
        first_name = df["Conversation"].iloc[0]
        assert first_name in name_list

    def test_groupDataframeByTimestamp(self, averages):
        timestamp_df = averages.groupDataframeByTimestamp()
        assert isinstance(timestamp_df, pd.Series)

    def test_createDictionaryWithProspectNamesAndListOfReplyTimes(
        self, averages, tracking
    ):
        dictionary_created = (
            averages.createDictionaryWithProspectNamesAndListOfReplyTimes()
        )
        df = tracking.dictionaryToDataframe()
        first_name = df["Conversation"].iloc[0]

        assert first_name in dictionary_created

    def test_getAverageReplyTimePerConversation(self, averages):
        reply_time_avg = averages.getAverageReplyTimePerConversation(
            "Abdulrahman Muhammad"
        )
        assert 86400000 > reply_time_avg > 1

    def test_getAverageReplyTimeOfAllConversations(self, averages):
        total_average = averages.getAverageReplyTimeOfAllConversations()
        assert isinstance(total_average, float) and 86400000 > total_average > 1

    def test_convertMstoMinutes(self, averages):
        total_average = averages.getAverageReplyTimeOfAllConversations()
        ms_response = averages.convertMstoMinutes(total_average)
        assert 1440 > ms_response > 0.009


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


class TestLeaderboard:
    def test_getWeekTotalromLevel10(self):
        data = Leaderboard(level_10).getWeekTotalFromLevel10()
        week_data = data["Week Total"].values
        sum_of_week_total = sum([i for i in week_data if isinstance(i, int)])
        assert isinstance(sum_of_week_total, int)

    def test_getDictionaryOfCellsToCheck(self):
        returned_dict = Leaderboard(level_10).getDictionaryOfCellsToCheck(
            role_dictionary
        )
        list_of_keys_in_dictionary = list(returned_dict.values())
        list_of_keys_in_data = list(
            Leaderboard(level_10).getWeekTotalFromLevel10().index.values
        )
        flattened_dictionary = [
            item for sublist in list_of_keys_in_dictionary for item in sublist
        ]
        assert all(elem in list_of_keys_in_data for elem in flattened_dictionary)

    def test_getValueForEachTeamMemberInTheirRole(self):
        df = Leaderboard(level_10).getValueForEachTeamMemberInTheirRole()
        frame_columns = list(df.columns)
        role_columns = list(role_dictionary.keys())
        assert role_columns == frame_columns

    def test_getSortedTCandSSNumbersForTeamMember(self):
        df = Leaderboard(level_10).getSortedTCandSSNumbersForTeamMember()
        basic_df = Leaderboard(level_10).getWeekTotalFromLevel10()

        girls_ss_sorted = int(df.loc["Girls SS"]["Pod Leads"])
        isela_ss_sorted = int(df.loc["Isela SS"]["Snr Specialists"])
        amanda_tc_sorted = int(df.loc["Amanda TC"]["Setters"])

        girls_ss_basic = int(basic_df.loc["Girls SS"]["Week Total"])
        isela_ss_basic = int(basic_df.loc["Isela SS"]["Week Total"])
        amanda_tc_basic = int(basic_df.loc["Amanda TC"]["Week Total"])

        girls_result = girls_ss_basic == girls_ss_sorted
        isela_result = isela_ss_basic == isela_ss_sorted
        amanda_result = amanda_tc_basic == amanda_tc_sorted

        assert all([girls_result, isela_result, amanda_result])


url = "https://api.oncehub.com/v2/bookings?expand=booking_page&limit=100"
headers = {
    "Accept": "application/json",
    "API-Key": "d7459f78d474f09276b4d708d2f2a161",
}
params = {"limit": 100}


class TestScheduleOnce:
    def test_getFullBookingList(self):
        booking_list = ScheduleOnce(url, headers).getFullBookingList()
        assert len(booking_list) == 100

    def test_getTCScheduledorTCBookedYesterday(self):
        booking_list = ScheduleOnce(url, headers).getTCScheduledorTCBookedYesterday()

        yesterday = str(datetime.date.today() - datetime.timedelta(1))

        starting_times = set()
        for f in booking_list:
            starting_times.add(f["starting_time"][0:10])

        starting = list(starting_times)[0]

        created = set()
        for f in booking_list:
            created.add(f["creation_time"][0:10])

        create = list(created)[0]
        assert create == yesterday or starting == yesterday

    def test_getBookingDataFromListOfBookings(self):
        booking_data = ScheduleOnce(url, headers).getBookingDataFromListOfBookings()
        assert not any(
            d["Page Name"] == "Big Rig Freight Services" for d in booking_data
        )

    def test_getValueCountsFromSourceOfPageName(self):
        booking_data = ScheduleOnce(url, headers).getValueCountsFromSourceOfPageName()
        indexes = list(booking_data.index)
        check = [item for item in indexes if item[0] == "Big Freight Services"]
        check2 = [item for item in indexes if item[1] == "Outbound Dial"]
        assert (len(check) > 0) and (len(check2) > 0)
