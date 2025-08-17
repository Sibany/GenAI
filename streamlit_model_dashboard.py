import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

# Load the QA comparison results
with open("qa_tool_comparison_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract true and predicted labels
true_labels = [entry["sms_conversations_last_tool_used"] for entry in data]
predicted_labels = [entry["test_result_last_tool_used"] for entry in data]

# Unique labels
all_labels = sorted(list(set(true_labels + predicted_labels)))

# Streamlit UI setup
st.set_page_config(page_title="Model Evaluation Dashboard", layout="wide")
st.title("📊 Model Evaluation Dashboard")
st.subheader("Performance Metrics and Visualizations")

# Sidebar label filter
st.sidebar.header("🔍 Filter Options")
selected_labels = st.sidebar.multiselect("Select Labels to Include", options=all_labels, default=all_labels)

# Filter data based on selected labels
filtered_data = [
    entry for entry in data
    if entry["sms_conversations_last_tool_used"] in selected_labels or entry["test_result_last_tool_used"] in selected_labels
]

filtered_true = [entry["sms_conversations_last_tool_used"] for entry in filtered_data]
filtered_pred = [entry["test_result_last_tool_used"] for entry in filtered_data]

# Accuracy
accuracy = accuracy_score(filtered_true, filtered_pred)
st.metric(label="✅ Overall Accuracy", value=f"{accuracy:.2%}")

# Confusion matrix
labels = sorted(list(set(filtered_true + filtered_pred)))
cm = confusion_matrix(filtered_true, filtered_pred, labels=labels)

st.markdown("### 🔄 Confusion Matrix Heatmap")
fig_cm, ax_cm = plt.subplots(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels, ax=ax_cm)
ax_cm.set_title("Confusion Matrix")
ax_cm.set_xlabel("Predicted Label")
ax_cm.set_ylabel("True Label")
st.pyplot(fig_cm)

# Classification report
report = classification_report(filtered_true, filtered_pred, output_dict=True)
report_df = pd.DataFrame(report).transpose()
st.markdown("### 📋 Classification Report")
st.dataframe(report_df, use_container_width=True)

# Class-wise precision chart
st.markdown("### 🎯 Class-wise Precision")
fig_prec, ax_prec = plt.subplots(figsize=(8, 5))
sns.barplot(x=report_df.index[:-3], y=report_df.loc[report_df.index[:-3], "precision"], ax=ax_prec)
ax_prec.set_title("Precision per Class")
ax_prec.set_ylabel("Precision")
ax_prec.set_xticklabels(ax_prec.get_xticklabels(), rotation=45)
st.pyplot(fig_prec)

# KPI metrics
kpi_data = []
for label in labels:
    tp = sum((t == label and p == label) for t, p in zip(filtered_true, filtered_pred))
    fp = sum((t != label and p == label) for t, p in zip(filtered_true, filtered_pred))
    fn = sum((t == label and p != label) for t, p in zip(filtered_true, filtered_pred))
    tn = sum((t != label and p != label) for t, p in zip(filtered_true, filtered_pred))
    kpi_data.append({
        "Label": label,
        "True Positives": tp,
        "False Positives": fp,
        "False Negatives": fn,
        "True Negatives": tn
    })

kpi_df = pd.DataFrame(kpi_data)
st.markdown("### 📊 KPI Metrics per Label")
st.dataframe(kpi_df, use_container_width=True)
