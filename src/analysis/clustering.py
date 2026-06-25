import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from src.data.config import OUTPUTS_DIR


def build_region_features(df: pd.DataFrame) -> pd.DataFrame:
    if "region" not in df.columns:
        raise ValueError("region column required")

    features = df.groupby("region").agg(
        total_alerts=("started_at", "size"),
        avg_duration=("duration_minutes", "mean"),
        max_duration=("duration_minutes", "max"),
        alert_days=("event_date", "nunique"),
    ).reset_index()

    features["alerts_per_day"] = features["total_alerts"] / features["alert_days"]
    features["avg_duration"] = features["avg_duration"].round(1)
    features["alerts_per_day"] = features["alerts_per_day"].round(2)

    return features


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    if "region" not in df.columns or "started_at" not in df.columns:
        raise ValueError("region and started_at columns required")

    daily_region = df.groupby([pd.Grouper(key="started_at", freq="D"), "region"]).size().unstack(fill_value=0)
    return daily_region.corr()


def cluster_regions(features: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    cluster_cols = ["total_alerts", "alerts_per_day", "avg_duration"]
    X = features[cluster_cols].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    features["cluster"] = kmeans.fit_predict(X_scaled)

    cluster_stats = features.groupby("cluster").agg(
        count=("region", "size"),
        avg_alerts=("total_alerts", "mean"),
        avg_frequency=("alerts_per_day", "mean"),
        avg_duration=("avg_duration", "mean"),
    ).round(1)

    print("\nCluster Statistics:")
    print(cluster_stats.to_string())

    return features


def find_optimal_k(features: pd.DataFrame, max_k: int = 8) -> int:
    cluster_cols = ["total_alerts", "alerts_per_day", "avg_duration"]
    X = features[cluster_cols].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    inertias = []
    K_range = range(2, min(max_k + 1, len(features)))

    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)

    deltas = np.diff(inertias)
    deltas2 = np.diff(deltas)
    optimal_k = K_range[np.argmax(deltas2) + 1] if len(deltas2) > 0 else 3

    return optimal_k


def plot_correlation_matrix(corr: pd.DataFrame, save: bool = True) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(14, 12))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

    sns.heatmap(
        corr,
        mask=mask,
        cmap="RdBu_r",
        center=0,
        annot=False,
        square=True,
        linewidths=0.5,
        ax=ax,
        vmin=-1,
        vmax=1,
        cbar_kws={"label": "Correlation"},
    )

    ax.set_title("Correlation Matrix Between Regions", fontsize=14, fontweight="bold")
    plt.tight_layout()

    if save:
        fig.savefig(OUTPUTS_DIR / "correlation_matrix.png", dpi=150, bbox_inches="tight")
    return fig


def plot_clusters(features: pd.DataFrame, save: bool = True) -> plt.Figure:
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    colors = sns.color_palette("Set2", features["cluster"].nunique())

    for cluster_id in sorted(features["cluster"].unique()):
        mask = features["cluster"] == cluster_id
        cluster_data = features[mask]

        axes[0].scatter(
            cluster_data["total_alerts"],
            cluster_data["avg_duration"],
            c=[colors[cluster_id]],
            label=f"Cluster {cluster_id}",
            s=100,
            edgecolors="white",
            linewidth=0.5,
        )

    axes[0].set_xlabel("Total Alerts", fontsize=11)
    axes[0].set_ylabel("Avg Duration (min)", fontsize=11)
    axes[0].set_title("Clusters: Alerts vs Duration", fontsize=12, fontweight="bold")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    for cluster_id in sorted(features["cluster"].unique()):
        mask = features["cluster"] == cluster_id
        cluster_data = features[mask]

        axes[1].scatter(
            cluster_data["total_alerts"],
            cluster_data["alerts_per_day"],
            c=[colors[cluster_id]],
            label=f"Cluster {cluster_id}",
            s=100,
            edgecolors="white",
            linewidth=0.5,
        )

    axes[1].set_xlabel("Total Alerts", fontsize=11)
    axes[1].set_ylabel("Alerts per Day", fontsize=11)
    axes[1].set_title("Clusters: Alerts vs Frequency", fontsize=12, fontweight="bold")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("Region Clustering (K-Means)", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()

    if save:
        fig.savefig(OUTPUTS_DIR / "clusters.png", dpi=150, bbox_inches="tight")
    return fig


def plot_elbow(features: pd.DataFrame, save: bool = True) -> plt.Figure:
    cluster_cols = ["total_alerts", "alerts_per_day", "avg_duration"]
    X = features[cluster_cols].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    inertias = []
    K_range = range(2, min(9, len(features)))

    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(K_range, inertias, "bo-", linewidth=2, markersize=8)
    ax.set_xlabel("Number of Clusters (k)", fontsize=11)
    ax.set_ylabel("Inertia", fontsize=11)
    ax.set_title("Elbow Method for Optimal k", fontsize=12, fontweight="bold")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save:
        fig.savefig(OUTPUTS_DIR / "elbow.png", dpi=150, bbox_inches="tight")
    return fig
