// anomalyTypes.js - Manages anomaly type options globally
export const anomalyOptions = [
  "",
  "Duplicate Transactions",
  "Missing Transactions",
  "Amount Discrepancies",
  "Unauthorized Transactions",
  "Date Mismatches",
  "Unbalanced Accounts",
  "Currency Conversion Errors",
  "Incorrect Account Postings",
  "Reversed Transactions",
  "Timing Differences",
  "Fraudulent Transactions",
  "Data Entry Errors",
  "Omitted Transactions",
  "System Integration Errors",
  "Policy Violations",
  "Threshold Breaches",
  "Suspicious Patterns",
  "Chargeback Anomalies",
  "Vendor Invoice Mismatches",
  "Bank Fee Errors"
];

export const addAnomalyType = (newType) => {
  if (!anomalyOptions.includes(newType)) {
    anomalyOptions.push(newType);
  }
};