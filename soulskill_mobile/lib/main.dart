import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'providers/resume_provider.dart';
import 'screens/home_screen.dart';
import 'theme/soulskill_theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const SoulSkillApp());
}

class SoulSkillApp extends StatelessWidget {
  const SoulSkillApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => ResumeProvider()..load(),
      child: MaterialApp(
        title: 'SoulSkill',
        debugShowCheckedModeBanner: false,
        theme: SoulSkillTheme.light,
        home: const HomeScreen(),
      ),
    );
  }
}
