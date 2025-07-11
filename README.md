
# US Critical Minerals Analytics

> End-to-end critical-minerals analytics on Microsoft Fabric from raw CSV to Power BI dashboards. Includes Lakehouse star-schema transformations, pipeline orchestration, a lake-based semantic model with DAX measures and RLS roles, and rich reporting—all version-controlled via GitHub.

## Description

This repository implements a **Medallion Architecture** in Microsoft Fabric to track the status of the U.S. government’s 2020-designated critical minerals. 

- **Bronze**: Raw CSV files ingested into the Lakehouse via pipeline.  
- **Silver**: PySpark-driven star schema transforms raw data into dimension and fact Delta tables.  
- **Gold**: A lake-based semantic model and Power BI reports providing certified, high-value analytics.

Built on Fabric, it shows how to ingest flat CSV data, transform it into curated schemas, orchestrate with pipelines, and deliver insights through a semantic layer and interactive dashboards.

This repository contains all artifacts for a production-ready analytics solution that tracks the status of the U.S. government’s 2020-designated critical minerals. Built on Microsoft Fabric, it demonstrates how to ingest flat CSV data, transform it into a star schema in Lakehouse, orchestrate workflows with Fabric pipelines, and deliver insights through a semantic model and interactive dashboards.

## Key Features

- **Automated Pipeline (`PL_Minerals`)**  
  - Copy Activity loads `mineral_ores.csv` to the Lakehouse.  
  - **Watermark-based Incremental Load**: only runs downstream steps when the CSV is new or modified by checking a JSON watermark in `/Files/watermarks/Watermark.json`.  
  - Notebook Activity runs PySpark to build dimension and fact tables.  
  - Model Refresh Activity updates the `SM_Minerals` semantic model.

- **Lakehouse Star Schema**  
  - Four dimension tables (`dim_commodities`, `dim_developments`, `dim_locations`, `dim_operations`).  
  - Fact table (`fact_minerals`) with calculated metrics (`ore_value`, `cost_per_ton`).

- **Semantic Model (`SM_Minerals`)**  
  - Connected to Lakehouse Delta tables.  
  - Custom DAX measures for KPI calculations and time intelligence.  
  - Display folders and hierarchies (Site – State – Region).  
  - Row-Level Security roles to control data access by user group.

- **Power BI Reporting**  
  - Interactive dashboards with maps, charts, and slicers.  
  - Anomaly detection flags for extraction cost outliers.  
  - Optimized with aggregations and direct query to semantic model.

- **GitHub Version Control**  
  - All notebooks, pipeline definitions, semantic model metadata, and Power BI files are tracked in Git.

## Watermark Implementation

> **Incremental logic** that prevents unnecessary pipeline runs by comparing file timestamps.

1. **Seed** a stub JSON file  
   - Path: `/Files/watermarks/Watermark.json`  
   - Contents:  
     ```json
     { "lastModified": "1970-01-01T00:00:00Z" }
     ```

2. **Lookup_Watermark**  
   - Reads `Watermark.json` into pipeline.

3. **GetMetadata_CSV**  
   - Retrieves the CSV’s current `lastModified` timestamp.

4. **IfNewData**  
   - Compares the two timestamps; only on “true” does the pipeline run copy → transform → refresh.

5. **Update_Watermark_Notebook**  
   - A PySpark notebook overwrites `Watermark.json` with the new timestamp, so subsequent runs use the updated watermark.

## Scheduling

The `PL_Minerals` pipeline is triggered on a schedule:

- **Trigger Name**: `DailyMineralsIngest`  
- **Frequency**: Daily at 08:00 UTC - 05:00 
- **Timezone**: Eastern Time (US and Canada)  

You can adjust or add additional triggers (e.g. hourly or on file-arrival events) in Fabric Studio under **Orchestrate → Triggers**.

## Folder Structure

```
mineral_analytics/                  # Root folder

├── core/                           # Core assets
│   ├── LH_Minerals/                # Lakehouse Delta table definitions
│   └── SM_Minerals/                # Semantic model metadata (DAX, RLS, hierarchies)
│
├── delivery/                       # Reporting artifacts
│   └── Minerals_Report/            # Power BI report (.pbix)
│
└── orchestration/                  # ETL & orchestration
    ├── PL_Minerals/                # Fabric pipeline JSON definitions
    ├── NB_Minerals/                # PySpark notebook for star schema transform
    └── NB_UpdateWatermark/         # PySpark notebook for watermark update (Watermark.json)
```

## Getting Started

1. **Clone** the repository:
   ```bash
   git clone https://github.com/your-org/mineral-analytics.git
   ```
2. **Configure** your Fabric workspace to connect to this repo via Git Integration.  
3. **Seed** the watermark:
   - In Fabric Studio **Data → Lakehouses → LH_Minerals → Files**, upload `Watermark.json` to `/watermarks` with:
     ```json
     { "lastModified": "1970-01-01T00:00:00Z" }
     ```
4. **Publish** all artifacts and **enable** the `DailyMineralsIngest` trigger.  
5. **Monitor** runs in **Orchestrate → Pipeline runs**; successful runs update both your Lakehouse tables and the watermark file.  
6. **Open** the Power BI file in `delivery/Minerals_Report` to view dashboards.

## Prerequisites

- Microsoft Fabric tenancy with Lakehouse, Pipelines, and Notebooks enabled.  
- Access to Azure Data Lake Gen2 storage.  
- Permissions to run PySpark notebooks and manage semantic models.  
- Power BI Desktop or Fabric-integrated report authoring.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repo and clone your fork.  
2. Create a branch: `feature/<your-feature>` or `fix/<issue>`.  
3. Add or update artifacts under the appropriate folder.  
4. Commit your changes with descriptive messages.  
5. Push to your fork and open a Pull Request against `main`.

## License

This project is licensed under the MIT License.
