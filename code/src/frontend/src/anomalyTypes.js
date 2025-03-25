// anomalyTypes.js - Manages anomaly type options globally
export const anomalyOptions = ["Break", "Leak", "Overheat", "Short Circuit"];

export const addAnomalyType = (newType) => {
  if (!anomalyOptions.includes(newType)) {
    anomalyOptions.push(newType);
  }
};