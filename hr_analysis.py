import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


sns.set_style("darkgrid")
pd.set_option("display.float_format", lambda x: f"{x:.2f}")

df = pd.read_csv("employees.csv")

df.columns = df.columns.str.strip()
df["Gender"].fillna("Unknown", inplace=True)
df["Team"].fillna("Unassigned", inplace=True)
df["Senior Management"].fillna(False, inplace=True)

df.dropna(subset=["First Name"], inplace=True)
df.drop_duplicates(inplace=True)

# Q1: Headcount by Team 

team_counts = df["Team"].value_counts().reset_index()
team_counts.columns = ["Team", "Headcount"]

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="Team", y="Headcount", data=team_counts, ax=ax)

ax.set_title("Headcount per Team")
ax.set_xlabel("Team")
ax.set_ylabel("Headcount")

for p in ax.patches:
    ax.annotate(
        f"{int(p.get_height())}",
        (p.get_x() + p.get_width() / 2, p.get_height()),
        ha="center", va="bottom",
        fontsize=9, fontweight="bold"
    )

ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig("q1_headcount_by_team.png", dpi=150, bbox_inches="tight")

# Q2: Salary Distribution 

fig2, ax2 = plt.subplots(1, 2, figsize=(10, 6))

sns.histplot(df, x="Salary", kde=True, ax=ax2[0], color="skyblue", edgecolor="black")
ax2[0].set_title("Salary Distribution")
ax2[0].axvline(df["Salary"].mean(), color="red", linestyle="--", label="Mean")
ax2[0].axvline(df["Salary"].median(), color="orange", linestyle="--", label="Median")
ax2[0].legend()

sns.boxplot(data=df, y="Salary", ax=ax2[1], color="lightgreen")
ax2[1].set_title("Salary Boxplot")

plt.tight_layout()
plt.savefig("q2_salary_distribution.png", dpi=150, bbox_inches="tight")

#  Q3: Average Salary by Team 

team_salary = df.groupby("Team")["Salary"].mean().reset_index()
team_salary.columns = ["Team", "Average Salary"]

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x="Team", y="Average Salary", data=team_salary, ax=ax3, palette="viridis")

ax3.set_title("Average Salary by Team")
ax3.tick_params(axis="x", rotation=45)

for p in ax3.patches:
    ax3.annotate(
        f"{p.get_height():,.0f}",
        (p.get_x() + p.get_width() / 2, p.get_height()),
        ha="center", va="bottom",
        fontsize=9, fontweight="bold"
    )

plt.tight_layout()
plt.savefig("q3_avg_salary_by_team.png", dpi=150, bbox_inches="tight")

#  Q4: Gender Pay Gap

df_gender = df[df["Gender"].isin(["Male", "Female"])]

gender_stats = (
    df_gender.groupby("Gender")["Salary"]
    .agg(Count="count", Avg_Salary="mean", Median="median")
    .reset_index()
)

fig4, axes = plt.subplots(1, 3, figsize=(18, 6))

sns.barplot(data=gender_stats, x="Gender", y="Avg_Salary",
            palette=["#4f8ef7", "#f778ba"], ax=axes[0])

sns.boxplot(data=df_gender, x="Gender", y="Salary",
            palette=["#4f8ef7", "#f778ba"], ax=axes[1])

gender_count = df_gender["Gender"].value_counts().reset_index()
gender_count.columns = ["Gender", "Count"]

sns.barplot(data=gender_count, x="Gender", y="Count",
            palette=["#4f8ef7", "#f778ba"], ax=axes[2])

plt.tight_layout()
plt.savefig("q4_gender_pay_gap.png", dpi=150, bbox_inches="tight")

#  Q5: Senior Management Analysis
senior_count = df["Senior Management"].value_counts().reset_index()
senior_count.columns = ["Senior Management", "Count"]
senior_count["Label"] = senior_count["Senior Management"].map(
    {True: "Senior Management", False: "Non-Senior"}
)

fig5, ax5 = plt.subplots(1, 2, figsize=(10, 6))

ax5[0].pie(
    senior_count["Count"],
    labels=senior_count["Label"],
    autopct="%1.1f%%",
    startangle=90,
    explode=[0, 0.05]
)

df_known = df[df["Gender"].isin(["Male", "Female"])]

mmgt_gender = (
    df_known.groupby(["Senior Management", "Gender"])
    .size()
    .reset_index(name="Count")
)

mmgt_gender["Role"] = mmgt_gender["Senior Management"].map(
    {True: "Senior Management", False: "Non-Senior"}
)

sns.barplot(data=mmgt_gender, x="Role", y="Count",
            hue="Gender", ax=ax5[1])

plt.tight_layout()
plt.savefig("q5_senior_management.png", dpi=150, bbox_inches="tight")

#  Q6: Bonus Analysis 
bonus_stats = (
    df.groupby("Team")["Bonus %"]
    .agg(avg="mean", min="min", max="max")
    .reset_index()
)

fig6, ax6 = plt.subplots(1, 2, figsize=(10, 6))

sns.barplot(data=bonus_stats, x="Team", y="avg", ax=ax6[0])
sns.boxplot(data=df, x="Team", y="Bonus %", ax=ax6[1])

plt.tight_layout()
plt.savefig("q6_bonus_analysis.png", dpi=150, bbox_inches="tight")

#  Q7: Top 10 Employees 
top_10 = df.sort_values("Salary", ascending=False).head(10).copy()
top_10["Bonus Amount"] = (top_10["Salary"] * top_10["Bonus %"] / 100).round(2)

fig7, ax7 = plt.subplots(1, 2, figsize=(14, 6))

sns.barplot(data=top_10, x="Salary", y="First Name",
            hue="Gender", legend=False, ax=ax7[0])

ax7[1].scatter(
    top_10["Salary"],
    top_10["Bonus Amount"],
    s=top_10["Bonus Amount"] * 10,
    alpha=0.6
)

plt.tight_layout()
plt.savefig("q7_top_10.png", dpi=150, bbox_inches="tight")

#  Q8: Senior Salary Comparison
df["Role"] = df["Senior Management"].map(
    {True: "Senior Management", False: "Non-Senior"}
)

senior_stats = (
    df.groupby("Role")["Salary"]
    .mean()
    .reset_index()
)

fig8, ax8 = plt.subplots(1, 3, figsize=(14, 6))

sns.barplot(data=senior_stats, x="Role", y="Salary", ax=ax8[0])
sns.violinplot(data=df, x="Role", y="Salary", ax=ax8[1])

team_mgmt = (
    df.groupby(["Team", "Role"])["Salary"]
    .mean()
    .reset_index()
)

sns.barplot(data=team_mgmt, x="Team", y="Salary",
            hue="Role", ax=ax8[2])

plt.tight_layout()
plt.savefig("q8_senior_management_salary.png", dpi=150, bbox_inches="tight")

# plt.show()


# 1. What is the exact correlation value
#    between Salary and Bonus %?
correlation = df["Salary"].corr(df["Bonus %"])
print(f"\nCorrelation between Salary and Bonus %: {correlation:.4f}")

# Interpret strength
if abs(correlation) < 0.2:
    strength = "Very Weak / No correlation"
elif abs(correlation) < 0.4:
    strength = "Weak correlation"
elif abs(correlation) < 0.6:
    strength = "Moderate correlation"
elif abs(correlation) < 0.8:
    strength = "Strong correlation"
else:
    strength = "Very Strong correlation"

print(f"Strength : {strength}")

# Direction
if correlation > 0:
    direction = "Positive — both go up together"
elif correlation < 0:
    direction = "Negative — one goes up, other goes down"
else:
    direction = "Flat — no relationship"
print(f"Direction: {direction}")

# Business interpretation
if abs(correlation) < 0.2:
    print("Business Meaning: Bonus % is awarded INDEPENDENTLY of salary")
    print("High earners do NOT necessarily get higher bonus %")
else:
    print("Business Meaning: Salary and bonus are related")

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Chart 1 — Heatmap
corr_matrix = df[["Salary", "Bonus %"]].corr()
sns.heatmap(corr_matrix,
            annot=True,
            fmt=".3f",
            cmap="coolwarm",
            linewidths=1,
            vmin=-1, vmax=1,
            square=True,
            annot_kws={"size": 14, "weight": "bold"},
            ax=axes[0])
axes[0].set_title("Correlation Heatmap",
                  fontsize=14, fontweight="bold")

# Chart 2 — Scatter with regression line
sns.regplot(data=df,
            x="Salary",
            y="Bonus %",
            scatter_kws={"alpha": 0.4,
                         "s": 40,
                         "color": "steelblue"},
            line_kws={"color": "red",
                      "linewidth": 2},
            ax=axes[1])
axes[1].set_title(f"Salary vs Bonus %\nCorrelation: {correlation:.3f}",
                  fontsize=13, fontweight="bold")
axes[1].set_xlabel("Salary (Rs)", fontsize=11)
axes[1].set_ylabel("Bonus %", fontsize=11)
axes[1].grid(True, linestyle="--", alpha=0.4)

fig.suptitle("Q9: Salary & Bonus Correlation Analysis",
             fontsize=16, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("q9_correlation.png", dpi=150, bbox_inches="tight")
plt.show()




# ════════════════════════════════════════════
# Q10: FULL HR ANALYTICS DASHBOARD
# ════════════════════════════════════════════
# ════════════════════════════════════════════
# Q10: FULL HR ANALYTICS DASHBOARD
 ════════════════════════════════════════════


correlation = df["Salary"].corr(df["Bonus %"])

fig = plt.figure(figsize=(24, 20))
fig.patch.set_facecolor("#0d1117")

from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch

gs = GridSpec(3, 3, figure=fig,
              hspace=0.45, wspace=0.35)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])
ax4 = fig.add_subplot(gs[1, 0])
ax5 = fig.add_subplot(gs[1, 1])
ax6 = fig.add_subplot(gs[1, 2])
ax7 = fig.add_subplot(gs[2, 0])
ax8 = fig.add_subplot(gs[2, 1])
ax9 = fig.add_subplot(gs[2, 2])


for ax in [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9]:
    ax.set_facecolor("#161b22")
    ax.tick_params(colors="white", labelsize=8)
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#30363d")

# ── Chart 1: Headcount by Team ──────────────
team_count = df["Team"].value_counts().reset_index()
team_count.columns = ["Team", "Count"]
sns.barplot(data=team_count, x="Team", y="Count",
            hue="Team", palette="Set2",
            legend=False, ax=ax1)
ax1.set_title("Headcount by Team",
              fontsize=11, fontweight="bold")
ax1.tick_params(axis="x", rotation=45, labelsize=7)
ax1.set_xlabel("")
ax1.grid(axis="y", linestyle="--", alpha=0.3)

# ── Chart 2: Salary Distribution ────────────
sns.histplot(data=df, x="Salary", bins=25,
             kde=True, color="steelblue",
             edgecolor="black", alpha=0.7, ax=ax2)
ax2.axvline(df["Salary"].mean(), color="red",
            linestyle="--", linewidth=1.5,
            label=f'Mean: {df["Salary"].mean():,.0f}')
ax2.set_title("Salary Distribution",
              fontsize=11, fontweight="bold")
ax2.legend(fontsize=7)
ax2.set_xlabel("Salary")
ax2.grid(axis="y", linestyle="--", alpha=0.3)

# ── Chart 3: Avg Salary by Team ─────────────
team_sal = (df.groupby("Team")["Salary"]
            .mean().reset_index()
            .sort_values("Salary", ascending=False))
sns.barplot(data=team_sal, x="Team", y="Salary",
            hue="Team", palette="Blues_d",
            legend=False, ax=ax3)
ax3.set_title("Avg Salary by Team",
              fontsize=11, fontweight="bold")
ax3.tick_params(axis="x", rotation=45, labelsize=7)
ax3.set_xlabel("")
ax3.grid(axis="y", linestyle="--", alpha=0.3)

# ── Chart 4: Gender Pay Gap ──────────────────
df_g = df[df["Gender"].isin(["Male","Female"])]
gender_avg = (df_g.groupby("Gender")["Salary"]
              .mean().reset_index())
sns.barplot(data=gender_avg, x="Gender", y="Salary",
            hue="Gender",
            palette={"Male":"#4f8ef7","Female":"#f778ba"},
            legend=False, ax=ax4)
ax4.set_title("Gender Pay Comparison",
              fontsize=11, fontweight="bold")
ax4.set_ylim(88000, 92000)
ax4.grid(axis="y", linestyle="--", alpha=0.3)
for p in ax4.patches:
    ax4.annotate(f"Rs {p.get_height():,.0f}",
                 (p.get_x() + p.get_width()/2,
                  p.get_height()),
                 ha="center", va="bottom",
                 fontsize=8, color="white",
                 fontweight="bold")

# ── Chart 5: Senior Management Pie ───────────
mgmt = df["Senior Management"].value_counts()
colors_pie = ["#4f8ef7", "#f0c040"]
ax5.pie(mgmt.values,
        labels=["Senior","Non-Senior"],
        autopct="%1.1f%%",
        colors=colors_pie,
        startangle=90,
        textprops={"color":"white","fontsize":9})
ax5.set_title("Senior Management Split",
              fontsize=11, fontweight="bold")

# ── Chart 6: Bonus % by Team ─────────────────
bonus_team = (df.groupby("Team")["Bonus %"]
              .mean().reset_index()
              .sort_values("Bonus %", ascending=False))
sns.barplot(data=bonus_team, x="Team", y="Bonus %",
            hue="Team", palette="YlOrRd",      # Fix 2
            legend=False, ax=ax6)
ax6.set_title("Avg Bonus % by Team",
              fontsize=11, fontweight="bold")
ax6.tick_params(axis="x", rotation=45, labelsize=7)
ax6.set_xlabel("")
ax6.grid(axis="y", linestyle="--", alpha=0.3)

# ── Chart 7: Top 10 Earners ──────────────────
top10 = df.nlargest(10, "Salary").sort_values(
    "Salary", ascending=True)
colors_bar = ["#f778ba" if g=="Female" else "#4f8ef7"
              for g in top10["Gender"]]
ax7.barh(top10["First Name"], top10["Salary"],
         color=colors_bar, edgecolor="black", height=0.6)
ax7.set_title("Top 10 Highest Earners",
              fontsize=11, fontweight="bold")
ax7.set_xlabel("Salary (Rs)")
ax7.grid(axis="x", linestyle="--", alpha=0.3)
ax7.legend(handles=[
    Patch(facecolor="#4f8ef7", label="Male"),
    Patch(facecolor="#f778ba", label="Female")
], fontsize=8)

# ── Chart 8: Senior vs Non-Senior ────────────
sns.violinplot(data=df,
               x="Senior Management",
               y="Salary",
               hue="Senior Management",  # Fix 2
               palette={True:"#4f8ef7", False:"#f0c040"},
               inner="box",
               legend=False,
               ax=ax8)
ax8.set_title("Senior vs Non-Senior Salary",
              fontsize=11, fontweight="bold")
ax8.set_xticks([0, 1])                   # Fix 3
ax8.set_xticklabels(["Non-Senior","Senior"])
ax8.grid(axis="y", linestyle="--", alpha=0.3)

# ── Chart 9: Salary vs Bonus ─────────────────
sns.regplot(data=df, x="Salary", y="Bonus %",
            scatter_kws={"alpha":0.3,"s":20,
                         "color":"steelblue"},
            line_kws={"color":"red","linewidth":2},
            ax=ax9)
ax9.set_title(f"Salary vs Bonus % (r={correlation:.2f})",
              fontsize=11, fontweight="bold")
ax9.grid(True, linestyle="--", alpha=0.3)

# ── Main Title ────────────────────────────────
fig.suptitle(
    "HR Analytics Dashboard  |  933 Employees",
    fontsize=22, fontweight="bold",
    color="white", y=0.98
)

# ── Insights Bar ─────────────────────────────
insights = (
    "KEY INSIGHTS:   "
    "No gender pay gap (1.25%)   |   "
    "Engineering highest paid   |   "
    "Unassigned team — investigate!   |   "
    "Seniority premium only 1.4%"
)
fig.text(0.5, 0.01, insights,
         ha="center", fontsize=9,
         color="#8b949e", style="italic")

plt.savefig("q10_hr_dashboard.png",
            dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.show()
