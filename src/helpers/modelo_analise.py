import pandas as pd

class ModelAnalisys:
    def get_features_pipe(pipeline, col_prev):
        # Get the trained model
        model = pipeline.named_steps["modelo"]

        # Get the selected feature mask or indices
        selected_mask = pipeline.named_steps["selecao"].get_support()
        selected_features = col_prev.columns[selected_mask]

        # Get feature importances and map to feature names
        importances = model.feature_importances_
        feature_importances = pd.Series(importances, index=selected_features).sort_values(ascending=True)
        return feature_importances