export const LOCATIONS = {
  Assam: {
    "Kamrup Metropolitan": [
      { id: "ward12", name: "Ward 12 (Demo — Live)", active: true },
      { id: "ward7", name: "Ward 7", active: true },
      { id: "ward15", name: "Ward 15", active: true },
    ],
    "Nagaon": [{ id: "nagaon-central", name: "Nagaon Central Ward", active: false }],
  },
  Bihar: { "Patna": [{ id: "patna-ward3", name: "Ward 3", active: false }] },
  "Uttar Pradesh": { "Gorakhpur": [{ id: "gkp-ward9", name: "Ward 9", active: false }] },
};

export const STATES = Object.keys(LOCATIONS);
export function getDistricts(state) { return state ? Object.keys(LOCATIONS[state] || {}) : []; }
export function getWards(state, district) { return state && district ? LOCATIONS[state]?.[district] || [] : []; }

export const SAMPLE_WARD_DATA = {
  ward7: {
    overallRisk: "LOW",
    sensors: [
      { id: "s1", location_name: "Ward 7 Culvert", sensor_code: "SEN-101", risk_level: "LOW", water_level_cm: 42, rainfall_mm_1h: 1, battery_percent: 91, last_updated: null },
      { id: "s2", location_name: "Ward 7 Overpass", sensor_code: "SEN-102", risk_level: "LOW", water_level_cm: 38, rainfall_mm_1h: 0, battery_percent: 88, last_updated: null },
    ],
  },
  ward15: {
    overallRisk: "MEDIUM",
    sensors: [
      { id: "s1", location_name: "Ward 15 Canal", sensor_code: "SEN-201", risk_level: "MEDIUM", water_level_cm: 98, rainfall_mm_1h: 14, battery_percent: 76, last_updated: null },
      { id: "s2", location_name: "Ward 15 Lowland", sensor_code: "SEN-202", risk_level: "LOW", water_level_cm: 51, rainfall_mm_1h: 3, battery_percent: 82, last_updated: null },
    ],
  },
};