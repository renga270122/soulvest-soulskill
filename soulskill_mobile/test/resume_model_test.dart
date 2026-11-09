import 'package:flutter_test/flutter_test.dart';
import 'package:soulskill_mobile/models/resume_model.dart';

void main() {
  group('ResumeModel migration and structured sections', () {
    test('reads legacy single-entry resume drafts', () {
      final resume = ResumeModel.fromJson({
        'fullName': 'Alex Morgan',
        'experienceRole': 'Engineer',
        'company': 'Acme',
        'experienceDescription': 'Built embedded systems',
        'degree': 'B.E.',
        'institution': 'Example University',
        'educationDetails': '2010',
      });

      expect(resume.effectiveWorkExperiences, hasLength(1));
      expect(resume.effectiveWorkExperiences.first['title'], 'Engineer');
      expect(resume.effectiveEducationEntries.first['institution'], 'Example University');
    });

    test('round trips projects and certifications through local JSON', () {
      const resume = ResumeModel(
        projects: [
          {'name': 'Device platform', 'description': 'Built a gateway', 'technologies': 'C++, STM32'}
        ],
        certifications: [
          {'name': 'Cloud Practitioner', 'issuer': 'Example', 'date': '2026'}
        ],
      );

      final restored = ResumeModel.fromJson(resume.toJson());
      expect(restored.projects.single['name'], 'Device platform');
      expect(restored.certifications.single['issuer'], 'Example');
    });

    test('includes all structured sections in the API payload', () {
      const resume = ResumeModel(
        workExperiences: [
          {'title': 'Lead', 'company': 'Acme', 'description': 'Led a team'}
        ],
        educationEntries: [
          {'degree': 'B.E.', 'institution': 'University', 'description': '2010'}
        ],
        projects: [
          {'name': 'Gateway', 'description': 'Built gateway', 'technologies': 'C++'}
        ],
        certifications: [
          {'name': 'Cloud', 'issuer': 'Provider', 'date': '2026'}
        ],
      );

      final payload = resume.toApiJson();
      expect((payload['work_experience'] as List), hasLength(1));
      expect((payload['education'] as List), hasLength(1));
      expect((payload['projects'] as List).single['name'], 'Gateway');
      expect((payload['certifications'] as List).single['name'], 'Cloud');
    });
  });
}
