import pandas as pd

class DataCollector:

    def __init__(self):
        pass

    def collect(self, path: str) -> pd.DataFrame:
        # Lecture du fichier Excel avec openpyxl
        df = pd.read_excel(path, engine="openpyxl")
        df.columns = [col.strip().lower() for col in df.columns]
        required_columns = {"time", "input_rate"}

        if not required_columns.issubset(df.columns):
            raise ValueError(
                f"Colonnes requises manquantes. Trouvées: {df.columns}"
            )

        df = df[["time", "input_rate"]].rename(
            columns={
                "time": "time",
                "input_rate": "input_rates"
            }
        )

        return df
