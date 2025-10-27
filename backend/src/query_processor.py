import pandas as pd
from typing import Dict, Any, List
from data_loader import DataLoader

class QueryProcessor:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def process_query(self, query_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the analyzed query and return results
        """
        if "error" in query_analysis:
            return query_analysis

        query_type = query_analysis.get("query_type", "")
        data_sources = query_analysis.get("data_sources", [])
        entities = query_analysis.get("entities", {})
        metrics = query_analysis.get("metrics", [])

        try:
            if query_type == "comparison":
                return self._handle_comparison(data_sources, entities, metrics)
            elif query_type == "ranking":
                return self._handle_ranking(data_sources, entities, metrics)
            elif query_type == "trend":
                return self._handle_trend(data_sources, entities, metrics)
            elif query_type == "correlation":
                return self._handle_correlation(data_sources, entities, metrics)
            else:
                return self._handle_general_query(data_sources, entities, metrics)

        except Exception as e:
            return {"error": f"Query processing failed: {str(e)}"}

    def _handle_comparison(self, data_sources: List[str], entities: Dict, metrics: List[str]) -> Dict:
        """Handle comparison queries"""
        results = {"query_type": "comparison", "data": []}

        if "rainfall" in data_sources:
            districts = entities.get("districts", [])
            rainfall_df = self.data_loader.get_rainfall_data()

            for district in districts:
                district_data = rainfall_df[rainfall_df['District'].str.contains(district, case=False, na=False)]
                if not district_data.empty:
                    row = district_data.iloc[0]
                    results["data"].append({
                        "district": row['District'],
                        "total_actual_rainfall": float(row['Total Actual Rainfall (June\'17 to May\'18) in mm']),
                        "total_normal_rainfall": float(row['Total Normal Rainfall (June\'17 to May\'18) in mm']),
                        "southwest_monsoon": float(row['Actual Rainfall in South West Monsoon (June\'17 to September\'17) in mm']),
                        "northeast_monsoon": float(row['Actual Rainfall in North East Monsoon (October\'17 to December\'17) in mm']),
                        "winter": float(row['Actual Rainfall in Winter Season (January\'18 to and February\'18) in mm']),
                        "hot_weather": float(row['Actual Rainfall in Hot Weather Season (March\'18 to May\'18) in mm'])
                    })

        if "crop" in data_sources:
            districts = entities.get("districts", [])
            crop_df = self.data_loader.get_crop_data()

            for district in districts:
                district_data = crop_df[crop_df['District Name'].str.contains(district, case=False, na=False)]
                if not district_data.empty:
                    row = district_data.iloc[0]
                    results["data"].append({
                        "district": row['District Name'],
                        "total_production": float(row['All Seasons_Production']),
                        "total_yield": float(row['All Seasons_Yield']),
                        "total_area": float(row['All Seasons_AreaAfter bund correction factor']),
                        "kharif_production": float(row['Kharif_Production']),
                        "rabi_production": float(row['Rabi_Production']),
                        "summer_production": float(row['Summer_Production'])
                    })

        return results

    def _handle_ranking(self, data_sources: List[str], entities: Dict, metrics: List[str]) -> Dict:
        """Handle ranking/top/highest/lowest queries"""
        results = {"query_type": "ranking", "data": []}

        if "crop" in data_sources:
            crop_df = self.data_loader.get_crop_data()

            # Exclude state total row
            crop_df = crop_df[crop_df['District Name'] != 'State Total']

            if "production" in metrics:
                # Sort by total production
                sorted_df = crop_df.sort_values('All Seasons_Production', ascending=False)
                top_10 = sorted_df.head(10)

                for _, row in top_10.iterrows():
                    results["data"].append({
                        "rank": len(results["data"]) + 1,
                        "district": row['District Name'],
                        "total_production": float(row['All Seasons_Production']),
                        "total_yield": float(row['All Seasons_Yield']),
                        "total_area": float(row['All Seasons_AreaAfter bund correction factor'])
                    })

            elif "yield" in metrics:
                sorted_df = crop_df.sort_values('All Seasons_Yield', ascending=False)
                top_10 = sorted_df.head(10)

                for _, row in top_10.iterrows():
                    results["data"].append({
                        "rank": len(results["data"]) + 1,
                        "district": row['District Name'],
                        "total_yield": float(row['All Seasons_Yield']),
                        "total_production": float(row['All Seasons_Production'])
                    })

        if "rainfall" in data_sources:
            rainfall_df = self.data_loader.get_rainfall_data()

            # Exclude state average
            rainfall_df = rainfall_df[rainfall_df['District'] != 'State Average']

            sorted_df = rainfall_df.sort_values('Total Actual Rainfall (June\'17 to May\'18) in mm', ascending=False)
            top_10 = sorted_df.head(10)

            for _, row in top_10.iterrows():
                results["data"].append({
                    "rank": len(results["data"]) + 1,
                    "district": row['District'],
                    "total_rainfall": float(row['Total Actual Rainfall (June\'17 to May\'18) in mm']),
                    "normal_rainfall": float(row['Total Normal Rainfall (June\'17 to May\'18) in mm'])
                })

        return results

    def _handle_trend(self, data_sources: List[str], entities: Dict, metrics: List[str]) -> Dict:
        """Handle trend analysis queries"""
        # Note: Current data is single time period, so trend analysis is limited
        return {
            "query_type": "trend",
            "message": "Trend analysis requires multi-year data. Current dataset contains single time period.",
            "data": []
        }

    def _handle_correlation(self, data_sources: List[str], entities: Dict, metrics: List[str]) -> Dict:
        """Handle correlation queries between crop and rainfall data"""
        results = {"query_type": "correlation", "data": [], "message": ""}

        # Note: Crop data is from Karnataka, rainfall data is from Tamil Nadu
        # Cannot directly correlate unless we have matching geographic data

        results["message"] = "Direct correlation not possible: Crop data is from Karnataka districts, rainfall data is from Tamil Nadu districts. Need matching geographic data for correlation analysis."

        return results

    def _handle_general_query(self, data_sources: List[str], entities: Dict, metrics: List[str]) -> Dict:
        """Handle general queries - provide summary statistics"""
        results = {"query_type": "general", "data": {}}

        if "crop" in data_sources:
            crop_df = self.data_loader.get_crop_data()
            crop_df = crop_df[crop_df['District Name'] != 'State Total']

            results["data"]["crop_summary"] = {
                "total_districts": len(crop_df),
                "total_production": float(crop_df['All Seasons_Production'].sum()),
                "avg_yield": float(crop_df['All Seasons_Yield'].mean()),
                "total_area": float(crop_df['All Seasons_AreaAfter bund correction factor'].sum()),
                "top_district": crop_df.loc[crop_df['All Seasons_Production'].idxmax(), 'District Name'],
                "top_production": float(crop_df['All Seasons_Production'].max())
            }

        if "rainfall" in data_sources:
            rainfall_df = self.data_loader.get_rainfall_data()
            rainfall_df = rainfall_df[rainfall_df['District'] != 'State Average']

            results["data"]["rainfall_summary"] = {
                "total_districts": len(rainfall_df),
                "avg_rainfall": float(rainfall_df['Total Actual Rainfall (June\'17 to May\'18) in mm'].mean()),
                "max_rainfall": float(rainfall_df['Total Actual Rainfall (June\'17 to May\'18) in mm'].max()),
                "min_rainfall": float(rainfall_df['Total Actual Rainfall (June\'17 to May\'18) in mm'].min()),
                "highest_rainfall_district": rainfall_df.loc[rainfall_df['Total Actual Rainfall (June\'17 to May\'18) in mm'].idxmax(), 'District']
            }

        return results
