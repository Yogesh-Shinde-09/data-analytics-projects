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

plt.show()