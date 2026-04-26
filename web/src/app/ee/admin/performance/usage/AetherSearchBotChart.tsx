import { ThreeDotsLoader } from "@/components/Loading";
import { getDatesList, useAetherSearchBotAnalytics } from "../lib";
import { DateRangePickerValue } from "@/components/dateRangeSelectors/AdminDateRangeSelector";
import { Text } from "@opal/components";
import Title from "@/components/ui/title";
import CardSection from "@/components/admin/CardSection";
import { AreaChartDisplay } from "@/components/ui/areaChart";

export function AetherSearchBotChart({
  timeRange,
}: {
  timeRange: DateRangePickerValue;
}) {
  const {
    data: aethersearchBotAnalyticsData,
    isLoading: isAetherSearchBotAnalyticsLoading,
    error: aethersearchBotAnalyticsError,
  } = useAetherSearchBotAnalytics(timeRange);

  let chart;
  if (isAetherSearchBotAnalyticsLoading) {
    chart = (
      <div className="h-80 flex flex-col">
        <ThreeDotsLoader />
      </div>
    );
  } else if (
    !aethersearchBotAnalyticsData ||
    aethersearchBotAnalyticsData[0] == undefined ||
    aethersearchBotAnalyticsError
  ) {
    chart = (
      <div className="h-80 text-red-600 text-bold flex flex-col">
        <p className="m-auto">Failed to fetch feedback data...</p>
      </div>
    );
  } else {
    const initialDate =
      timeRange.from || new Date(aethersearchBotAnalyticsData[0].date);
    const dateRange = getDatesList(initialDate);

    const dateToAetherSearchBotAnalytics = new Map(
      aethersearchBotAnalyticsData.map((aethersearchBotAnalyticsEntry) => [
        aethersearchBotAnalyticsEntry.date,
        aethersearchBotAnalyticsEntry,
      ])
    );

    chart = (
      <AreaChartDisplay
        className="mt-4"
        data={dateRange.map((dateStr) => {
          const aethersearchBotAnalyticsForDate = dateToAetherSearchBotAnalytics.get(dateStr);
          return {
            Day: dateStr,
            "Total Queries": aethersearchBotAnalyticsForDate?.total_queries || 0,
            "Automatically Resolved":
              aethersearchBotAnalyticsForDate?.auto_resolved || 0,
          };
        })}
        categories={["Total Queries", "Automatically Resolved"]}
        index="Day"
        colors={["indigo", "fuchsia"]}
        yAxisWidth={60}
      />
    );
  }

  return (
    <CardSection className="mt-8">
      <Title>Slack Channel</Title>
      <Text as="p">Total Queries vs Auto Resolved</Text>
      {chart}
    </CardSection>
  );
}
