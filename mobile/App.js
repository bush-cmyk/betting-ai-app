import React, { useMemo, useState } from "react";
import {
  ActivityIndicator,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";

const API_BASE_URL =
  process.env.EXPO_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

function NumberField({ label, value, onChangeText, hint }) {
  return (
    <View style={styles.field}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        style={styles.input}
        value={value}
        onChangeText={onChangeText}
        keyboardType="decimal-pad"
        placeholder={hint}
      />
    </View>
  );
}

export default function App() {
  const [homeForm, setHomeForm] = useState("0.80");
  const [awayForm, setAwayForm] = useState("0.55");
  const [homeStrength, setHomeStrength] = useState("84");
  const [awayStrength, setAwayStrength] = useState("77");
  const [homeAdvantage, setHomeAdvantage] = useState(true);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const canSubmit = useMemo(() => {
    const values = [
      Number(homeForm),
      Number(awayForm),
      Number(homeStrength),
      Number(awayStrength),
    ];
    return values.every((value) => Number.isFinite(value));
  }, [homeForm, awayForm, homeStrength, awayStrength]);

  async function predict() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          home_form: Number(homeForm),
          away_form: Number(awayForm),
          home_strength: Number(homeStrength),
          away_strength: Number(awayStrength),
          home_advantage: homeAdvantage,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail ? JSON.stringify(data.detail) : "Prediction failed"
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        `${err.message}. Check that the backend is running at ${API_BASE_URL}.`
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.container}>
        <Text style={styles.eyebrow}>PORTFOLIO DEMO</Text>
        <Text style={styles.title}>SportsAI Simulator</Text>
        <Text style={styles.subtitle}>
          Enter sample team indicators and request an AI-generated outcome
          simulation.
        </Text>

        <View style={styles.card}>
          <NumberField
            label="Home form (0–1)"
            value={homeForm}
            onChangeText={setHomeForm}
            hint="0.80"
          />
          <NumberField
            label="Away form (0–1)"
            value={awayForm}
            onChangeText={setAwayForm}
            hint="0.55"
          />
          <NumberField
            label="Home strength (0–100)"
            value={homeStrength}
            onChangeText={setHomeStrength}
            hint="84"
          />
          <NumberField
            label="Away strength (0–100)"
            value={awayStrength}
            onChangeText={setAwayStrength}
            hint="77"
          />

          <Text style={styles.label}>Home advantage</Text>
          <View style={styles.toggleRow}>
            <TouchableOpacity
              style={[
                styles.toggleButton,
                homeAdvantage && styles.toggleButtonActive,
              ]}
              onPress={() => setHomeAdvantage(true)}
            >
              <Text
                style={[
                  styles.toggleText,
                  homeAdvantage && styles.toggleTextActive,
                ]}
              >
                Yes
              </Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.toggleButton,
                !homeAdvantage && styles.toggleButtonActive,
              ]}
              onPress={() => setHomeAdvantage(false)}
            >
              <Text
                style={[
                  styles.toggleText,
                  !homeAdvantage && styles.toggleTextActive,
                ]}
              >
                No
              </Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            style={[
              styles.primaryButton,
              (!canSubmit || loading) && styles.primaryButtonDisabled,
            ]}
            disabled={!canSubmit || loading}
            onPress={predict}
          >
            {loading ? (
              <ActivityIndicator />
            ) : (
              <Text style={styles.primaryButtonText}>Run Prediction</Text>
            )}
          </TouchableOpacity>
        </View>

        {error ? (
          <View style={styles.errorCard}>
            <Text style={styles.errorText}>{error}</Text>
          </View>
        ) : null}

        {result ? (
          <View style={styles.resultCard}>
            <Text style={styles.resultLabel}>Predicted outcome</Text>
            <Text style={styles.resultValue}>{result.predicted_outcome}</Text>
            <Text style={styles.confidence}>
              Confidence: {(result.confidence * 100).toFixed(1)}%
            </Text>

            <View style={styles.probabilityList}>
              {Object.entries(result.probabilities).map(([key, value]) => (
                <View key={key} style={styles.probabilityRow}>
                  <Text style={styles.probabilityName}>{key}</Text>
                  <Text style={styles.probabilityValue}>
                    {(value * 100).toFixed(1)}%
                  </Text>
                </View>
              ))}
            </View>

            <Text style={styles.modelSource}>
              Source: {result.model_source}
            </Text>
          </View>
        ) : null}

        <Text style={styles.disclaimer}>
          Educational simulation only. This application does not place wagers
          and does not provide financial or betting advice.
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: "#0b1020",
  },
  container: {
    padding: 22,
    paddingBottom: 40,
  },
  eyebrow: {
    color: "#9fb0d0",
    fontSize: 12,
    fontWeight: "700",
    letterSpacing: 2,
    marginTop: 16,
  },
  title: {
    color: "#ffffff",
    fontSize: 34,
    fontWeight: "800",
    marginTop: 8,
  },
  subtitle: {
    color: "#b9c4db",
    fontSize: 16,
    lineHeight: 23,
    marginTop: 8,
    marginBottom: 22,
  },
  card: {
    backgroundColor: "#151d33",
    borderRadius: 18,
    padding: 18,
  },
  field: {
    marginBottom: 14,
  },
  label: {
    color: "#dce5f7",
    fontSize: 14,
    fontWeight: "600",
    marginBottom: 7,
  },
  input: {
    backgroundColor: "#ffffff",
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 16,
  },
  toggleRow: {
    flexDirection: "row",
    gap: 10,
    marginBottom: 18,
  },
  toggleButton: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#7282a5",
    borderRadius: 10,
    paddingVertical: 11,
    alignItems: "center",
  },
  toggleButtonActive: {
    backgroundColor: "#d8e1f5",
  },
  toggleText: {
    color: "#d8e1f5",
    fontWeight: "700",
  },
  toggleTextActive: {
    color: "#0b1020",
  },
  primaryButton: {
    backgroundColor: "#ffffff",
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: "center",
  },
  primaryButtonDisabled: {
    opacity: 0.5,
  },
  primaryButtonText: {
    color: "#0b1020",
    fontWeight: "800",
    fontSize: 16,
  },
  errorCard: {
    marginTop: 16,
    backgroundColor: "#311a20",
    borderRadius: 14,
    padding: 16,
  },
  errorText: {
    color: "#ffd5dc",
    lineHeight: 20,
  },
  resultCard: {
    marginTop: 16,
    backgroundColor: "#ffffff",
    borderRadius: 18,
    padding: 18,
  },
  resultLabel: {
    color: "#657089",
    fontWeight: "600",
  },
  resultValue: {
    color: "#0b1020",
    fontSize: 30,
    fontWeight: "800",
    marginTop: 4,
  },
  confidence: {
    color: "#36415a",
    marginTop: 4,
    marginBottom: 14,
  },
  probabilityList: {
    borderTopWidth: 1,
    borderTopColor: "#e3e7ef",
    paddingTop: 10,
  },
  probabilityRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 5,
  },
  probabilityName: {
    color: "#36415a",
  },
  probabilityValue: {
    color: "#0b1020",
    fontWeight: "700",
  },
  modelSource: {
    color: "#7a8499",
    fontSize: 12,
    marginTop: 12,
  },
  disclaimer: {
    color: "#8794af",
    fontSize: 12,
    lineHeight: 18,
    textAlign: "center",
    marginTop: 22,
  },
});
