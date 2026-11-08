import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:soulskill_mobile/main.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  testWidgets('shows responsive SoulSkill dashboard and opens Resume Studio',
      (tester) async {
    await tester.pumpWidget(const SoulSkillApp());
    await tester.pumpAndSettle();

    expect(find.text('SoulSkill'), findsOneWidget);
    expect(find.text('Welcome to your next chapter'), findsOneWidget);
    expect(find.text('Create / improve resume'), findsOneWidget);
    await tester.tap(find.text('Create / improve resume'));
    await tester.pumpAndSettle();

    expect(find.text('Resume Studio'), findsOneWidget);
    expect(find.text('Personal details'), findsOneWidget);
  });

  testWidgets('opens SoulMind and completes the guided reflection',
      (tester) async {
    await tester.pumpWidget(const SoulSkillApp());
    await tester.pumpAndSettle();

    await tester.tap(find.text('SoulMind').last);
    await tester.pumpAndSettle();

    expect(find.text('TODAY’S AFFIRMATION'), findsOneWidget);
    await tester.ensureVisible(find.text('Begin a 2-minute reflection'));
    await tester.pumpAndSettle();
    expect(find.text('Begin a 2-minute reflection'), findsOneWidget);

    await tester.tap(find.text('Begin a 2-minute reflection'));
    await tester.pumpAndSettle();

    expect(find.text('I’m sorry.'), findsOneWidget);
    await tester.tap(find.text('Continue'));
    await tester.pumpAndSettle();
    expect(find.text('Please forgive me.'), findsOneWidget);
    await tester.tap(find.text('Continue'));
    await tester.pumpAndSettle();
    expect(find.text('Thank you.'), findsOneWidget);
    await tester.tap(find.text('Continue'));
    await tester.pumpAndSettle();
    expect(find.text('I love you.'), findsOneWidget);

    await tester.tap(find.text('Complete reflection'));
    await tester.pumpAndSettle();
    expect(find.text('Begin a 2-minute reflection'), findsOneWidget);
  });

  testWidgets('uses desktop navigation at wide viewport', (tester) async {
    tester.view.physicalSize = const Size(1440, 1000);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(const SoulSkillApp());
    await tester.pumpAndSettle();

    expect(find.text('WORKSPACE'), findsOneWidget);
    expect(find.text('Career Studio'), findsOneWidget);
    expect(find.text('A global career workspace'), findsOneWidget);

    await tester.tap(find.text('SoulMind').first);
    await tester.pumpAndSettle();
    expect(find.text('Affirmations for your journey'), findsOneWidget);
  });
}
