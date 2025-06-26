import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set Streamlit config
st.set_page_config(page_title="F1 2024 Dashboard", layout="wide")

# Load the data
df = pd.read_csv("f1.csv")  # Use your exact CSV filename

# title
st.title(("🏁 F1 2024 Season Dashboard"))
st.markdown("Explore the performance of the Drivers and Constructors in the 2024 F1 season.")

# Assuming df is already loaded above this
driver_points = df.groupby('Driver', as_index=False)[['Points']].sum()
driver_points = driver_points.sort_values(by='Points', ascending=False)

# ✅ Create the plot
fig, ax = plt.subplots(figsize=(12, 6))
driver_points.plot(
    x='Driver',
    y='Points',
    kind='bar',
    ax=ax,
    color='orange'
)
ax.set_title("Total Points by Driver - F1 2024")
ax.set_xlabel("Driver")
ax.set_ylabel("Points")
plt.xticks(rotation=45, ha='right')
plt.axhline(0, color='gray', linestyle='--')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

# ✅ Now show the plot and observations side-by-side
col1, col2 = st.columns([3, 3])

with col1:
    st.pyplot(fig)

with col2:
    st.markdown("### 🏁  Total Points by Driver")
    st.markdown("""
    - **Verstappen** led the season with a dominant points tally.  
    - **Norris** and **Leclerc** followed as close contenders for 2nd.  
    - Midfield drivers trailed with a noticeable gap in performance.  

    💡 **Conclusion:** 
    *Driver points reflect both speed and consistency across the season.*
    """)

# Assuming df is already loaded above this
constructor_points = df.groupby('Team', as_index = False)[['Points']].sum()
constructor_points = constructor_points.sort_values(by='Points', ascending=False)

# ✅ Create the plot
fig2, ax = plt.subplots(figsize=(12, 6))
constructor_points.plot(
    x='Team',
    y='Points',
    kind='bar',
    ax=ax,
    color='steelblue'
)

ax.set_title("Total Points by Constructors - F1 2024")
ax.set_xlabel("Constructor")
ax.set_ylabel("Points")
plt.xticks(rotation=45, ha='right')
plt.axhline(0, color='gray', linestyle='--')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

col3, col4 = st.columns([3,3])

with col3:
    st.pyplot(fig2)

with col4:
    st.markdown("###  🏎️ Constructor Standings")
    st.markdown("""
    - 🏆 **McLaren** took the title with consistent performances from both drivers.  
    - **Red Bull** underperformed as **Pérez** struggled despite **Verstappen's** dominance.  
    - **Mercedes** showed stable but below-par results compared to past glory.  
    💡 **Conclusion:**
The points distribution reveals a clear hierarchy in driver performance throughout the season, with Verstappen clearly in a league of his own, followed by a tight battle in the upper midfield.
    """)


# ✅ Clean 'Position' column: Convert to numeric, turn 'NC' or non-numeric to NaN
df['Position'] = pd.to_numeric(df['Position'], errors='coerce')

# ✅ Group by driver and calculate standard deviation of finishing positions
driver_consistency = df.groupby('Driver', as_index=False)['Position'].std()
driver_consistency = driver_consistency.sort_values(by='Position')
driver_consistency.rename(columns={'Position': 'Std_Dev_Position'}, inplace=True)

# ✅ Create the plot
fig3, ax = plt.subplots(figsize=(12, 6))
ax.bar(driver_consistency['Driver'], driver_consistency['Std_Dev_Position'], color='mediumseagreen')
ax.set_title("Driver Consistency (Standard Deviation of Finishing Position) - F1 2024")
ax.set_xlabel("Driver")
ax.set_ylabel("Standard Deviation")
plt.xticks(rotation=45, ha='right')
plt.axhline(0, color='gray', linestyle='--')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

# ✅ Show plot and observations side-by-side
col5, col6 = st.columns([3, 3])

with col5:
    st.pyplot(fig3)

with col6:
    st.markdown("### 🧠  Driver Consistency (Standard Deviation of Finishing Position)")
    st.markdown("""

        🔍 **Observations:**

        1. Lower standard deviation = more consistent finishes.
        2. **Franco Colapinto** ranks highest in consistency, likely due to fewer races.
        3. **Max Verstappen** shows top-level consistency, matching his dominance.
        4. **Valtteri Bottas** is consistent, but at the back of the field.

        💡 **Conclusion:**  
        Consistency plays a major role in a driver's season. Some drivers were reliably strong, others consistently mid or low — both patterns have different implications.

    """)

# Plot 5 - Average Grid Gain/Loss
# Make sure 'Grid_gain' column is numeric (just in case)
# Make sure 'Grid' and 'Position' columns exist and are numeric
# Convert Position and Grid columns to numeric (handle non-numeric cases safely)
# Convert Position and Starting Grid columns to numeric
# Convert to numeric in case there are stray strings
df['Position'] = pd.to_numeric(df['Position'], errors='coerce')
df['Starting Grid'] = pd.to_numeric(df['Starting Grid'], errors='coerce')

# Create Grid_gain column (Starting Grid - Position)
df['Grid_gain'] = df['Starting Grid'] - df['Position']

# Group by Driver and get average gain/loss
avg_grid_gain = df.groupby('Driver', as_index=False)['Grid_gain'].mean()
avg_grid_gain = avg_grid_gain.sort_values(by='Grid_gain', ascending=False)

# Plot
fig4, ax = plt.subplots(figsize=(12, 6))
avg_grid_gain.plot(
    x='Driver',
    y='Grid_gain',
    kind='bar',
    color='mediumseagreen',
    edgecolor='black',
    ax=ax
)
ax.set_title('Average Grid Gain/Loss per Race - F1 2024')
ax.set_xlabel('Driver')
ax.set_ylabel('Avg Grid Gain')
plt.xticks(rotation=45, ha='right')
plt.axhline(0, color='gray', linestyle='--')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

# Display side-by-side in Streamlit
col7, col8 = st.columns([3, 3])

with col7:
    st.pyplot(fig4)

with col8:
    st.markdown("### 🔺🔻 Racecraft – Average Grid Gain/Loss")
    st.markdown("""
    🔍 **Observations:**

    - **Franco Colapinto** had the highest average grid gain — a rookie outperforming expectations.
    - **Lewis Hamilton** showed strong racecraft, gaining many positions despite starting mid-grid.
    - **VCARB drivers** lost positions on average, hinting at poor race pace or reliability.

    💡 **Conclusion:**  
    Grid gain isn't just about speed — it's about strategy, adaptability, and execution on race day.
    """)


# ✅ Fastest Laps by Driver Plot
fastest_laps_only = df[df['Set Fastest Lap'] == 'Yes']
fastest_lap_count = fastest_laps_only['Driver'].value_counts()

fig6, ax = plt.subplots(figsize=(12, 6))
fastest_lap_count.plot(
    kind='bar',
    color='darkviolet',
    edgecolor='black',
    ax=ax
)
ax.set_title("Fastest Laps by Driver - F1 2024")
ax.set_xlabel("Driver")
ax.set_ylabel("Fastest Laps")
plt.xticks(rotation=45, ha='right')
plt.axhline(0, color='gray', linestyle='--')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

col9, col10 = st.columns([3, 3])

with col9:
    st.pyplot(fig6)

with col10:
    st.markdown("### ⚡ Fastest Laps by Driver")
    st.markdown("""
    - **Lando Norris** leads in fastest laps, reflecting McLaren’s late-season form.  
    - **Verstappen** and **Leclerc** follow closely — showing pace, but with differing team consistency.  
    - **Alonso's** position signals Aston Martin’s occasional speed despite inconsistent results.  
    💡 **Conclusion:**  
     *Fastest laps show raw speed, but strategy and consistency shape championship success.*
    """)


# ✅ DNFs by Driver Plot
dnfs = df[df['Time/Retired'] == 'DNF']
dnf_count = dnfs['Driver'].value_counts()

fig7, ax = plt.subplots(figsize=(12, 6))
dnf_count.plot(
    kind='bar',
    color='crimson',
    edgecolor='black',
    ax=ax
)
ax.set_title("Total DNFs by Driver - F1 2024")
ax.set_xlabel("Driver")
ax.set_ylabel("DNFs")
plt.xticks(rotation=45, ha='right')
plt.axhline(0, color='gray', linestyle='--')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

col11, col12 = st.columns([3, 3])

with col11:
    st.pyplot(fig7)

with col12:
    st.markdown("### ❌ DNFs by Driver")
    st.markdown("""
    - **Albon** tops the DNF chart — Williams' season focused more on testing than results.  
    - **Sergio Perez** struggled with 5 DNFs, linked to Red Bull's car setup favoring Verstappen.  
    - **Tsunoda**’s DNFs stemmed from both reliability issues and driving errors.  
    💡 **Conclusion:**  
    *DNFs reflect not just driver mistakes but also team reliability — both crucial in the championship battle.*
    """)
