import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const SportsAiApp());
}

class SportsAiApp extends StatelessWidget {
  const SportsAiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'SportsAI Simulator',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.indigo,
          brightness: Brightness.dark,
        ),
      ),
      home: const PredictionPage(),
    );
  }
}

class PredictionPage extends StatefulWidget {
  const PredictionPage({super.key});

  @override
  State<PredictionPage> createState() => _PredictionPageState();
}

class _PredictionPageState extends State<PredictionPage> {
  final homeFormController = TextEditingController(text: '0.80');
  final awayFormController = TextEditingController(text: '0.55');
  final homeStrengthController = TextEditingController(text: '84');
  final awayStrengthController = TextEditingController(text: '77');

  bool homeAdvantage = true;
  bool loading = false;

  String? predictedOutcome;
  double? confidence;
  Map<String, dynamic>? probabilities;
  String? modelSource;
  String? errorMessage;

  final String apiUrl = 'http://127.0.0.1:8000/predict';

  Future<void> runPrediction() async {
    setState(() {
      loading = true;
      errorMessage = null;
      predictedOutcome = null;
    });

    try {
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'home_form': double.parse(homeFormController.text),
          'away_form': double.parse(awayFormController.text),
          'home_strength': double.parse(homeStrengthController.text),
          'away_strength': double.parse(awayStrengthController.text),
          'home_advantage': homeAdvantage,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        setState(() {
          predictedOutcome = data['predicted_outcome'];
          confidence = (data['confidence'] as num).toDouble();
          probabilities =
              Map<String, dynamic>.from(data['probabilities']);
          modelSource = data['model_source'];
        });
      } else {
        setState(() {
          errorMessage =
              'Prediction failed. HTTP ${response.statusCode}';
        });
      }
    } catch (error) {
      setState(() {
        errorMessage =
            'Could not connect to the SportsAI backend.\n$error';
      });
    } finally {
      setState(() {
        loading = false;
      });
    }
  }

  @override
  void dispose() {
    homeFormController.dispose();
    awayFormController.dispose();
    homeStrengthController.dispose();
    awayStrengthController.dispose();
    super.dispose();
  }

  Widget buildInput(
    String label,
    TextEditingController controller,
  ) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: TextField(
        controller: controller,
        keyboardType:
            const TextInputType.numberWithOptions(decimal: true),
        decoration: InputDecoration(
          labelText: label,
          border: const OutlineInputBorder(),
        ),
      ),
    );
  }

  Widget probabilityRow(String label) {
    final value = probabilities?[label];

    if (value == null) {
      return const SizedBox.shrink();
    }

    final percent = ((value as num).toDouble() * 100);

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label),
          Text(
            '${percent.toStringAsFixed(1)}%',
            style: const TextStyle(
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 650),
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Text(
                    'PORTFOLIO DEMO',
                    style: TextStyle(
                      letterSpacing: 2,
                      fontWeight: FontWeight.bold,
                      color: Colors.white60,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'SportsAI Simulator',
                    style: TextStyle(
                      fontSize: 36,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 10),
                  const Text(
                    'Enter sample team indicators and request an '
                    'AI-generated sports outcome simulation.',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.white70,
                    ),
                  ),
                  const SizedBox(height: 30),

                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: Column(
                        children: [
                          buildInput(
                            'Home form (0–1)',
                            homeFormController,
                          ),
                          buildInput(
                            'Away form (0–1)',
                            awayFormController,
                          ),
                          buildInput(
                            'Home strength (0–100)',
                            homeStrengthController,
                          ),
                          buildInput(
                            'Away strength (0–100)',
                            awayStrengthController,
                          ),

                          SwitchListTile(
                            title: const Text('Home advantage'),
                            value: homeAdvantage,
                            onChanged: (value) {
                              setState(() {
                                homeAdvantage = value;
                              });
                            },
                          ),

                          const SizedBox(height: 12),

                          SizedBox(
                            width: double.infinity,
                            child: FilledButton(
                              onPressed:
                                  loading ? null : runPrediction,
                              child: Padding(
                                padding:
                                    const EdgeInsets.all(14),
                                child: loading
                                    ? const CircularProgressIndicator()
                                    : const Text(
                                        'Run Prediction',
                                        style: TextStyle(
                                          fontSize: 16,
                                          fontWeight:
                                              FontWeight.bold,
                                        ),
                                      ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),

                  if (errorMessage != null) ...[
                    const SizedBox(height: 20),
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(20),
                        child: Text(
                          errorMessage!,
                          style: const TextStyle(
                            color: Colors.redAccent,
                          ),
                        ),
                      ),
                    ),
                  ],

                  if (predictedOutcome != null) ...[
                    const SizedBox(height: 20),

                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(22),
                        child: Column(
                          crossAxisAlignment:
                              CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Predicted outcome',
                              style: TextStyle(
                                color: Colors.white70,
                              ),
                            ),

                            const SizedBox(height: 6),

                            Text(
                              predictedOutcome!,
                              style: const TextStyle(
                                fontSize: 34,
                                fontWeight: FontWeight.bold,
                              ),
                            ),

                            const SizedBox(height: 8),

                            Text(
                              'Confidence: '
                              '${(confidence! * 100).toStringAsFixed(1)}%',
                            ),

                            const Divider(height: 30),

                            probabilityRow('HOME'),
                            probabilityRow('DRAW'),
                            probabilityRow('AWAY'),

                            const SizedBox(height: 15),

                            Text(
                              'Source: $modelSource',
                              style: const TextStyle(
                                color: Colors.white54,
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],

                  const SizedBox(height: 24),

                  const Text(
                    'Educational simulation only. '
                    'This application does not place wagers and '
                    'does not provide financial or betting advice.',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: Colors.white54,
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}