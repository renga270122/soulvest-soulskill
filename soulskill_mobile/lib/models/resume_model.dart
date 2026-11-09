class ResumeModel {
  const ResumeModel({
    this.fullName = '',
    this.targetRole = '',
    this.email = '',
    this.phone = '',
    this.location = '',
    this.professionalSummary = '',
    this.experienceRole = '',
    this.company = '',
    this.experienceDescription = '',
    this.degree = '',
    this.institution = '',
    this.educationDetails = '',
    this.workExperiences = const [],
    this.educationEntries = const [],
    this.skills = '',
    this.updatedAt = '',
  });

  final String fullName, targetRole, email, phone, location, professionalSummary;
  // Legacy fields remain readable so older screens and saved drafts stay compatible.
  final String experienceRole, company, experienceDescription;
  final String degree, institution, educationDetails;
  final List<Map<String, String>> workExperiences;
  final List<Map<String, String>> educationEntries;
  final String skills, updatedAt;

  List<Map<String, String>> get effectiveWorkExperiences =>
      workExperiences.isNotEmpty ? workExperiences : [
        if (experienceRole.isNotEmpty || company.isNotEmpty || experienceDescription.isNotEmpty)
          {'title': experienceRole, 'company': company, 'description': experienceDescription}
      ];

  List<Map<String, String>> get effectiveEducationEntries =>
      educationEntries.isNotEmpty ? educationEntries : [
        if (degree.isNotEmpty || institution.isNotEmpty || educationDetails.isNotEmpty)
          {'degree': degree, 'institution': institution, 'description': educationDetails}
      ];

  List<String> get skillList => skills.split(',').map((s) => s.trim())
      .where((s) => s.isNotEmpty).toSet().toList();

  int get completionPercent {
    final checks = <bool>[
      fullName.trim().isNotEmpty, targetRole.trim().isNotEmpty,
      email.trim().isNotEmpty, phone.trim().isNotEmpty,
      professionalSummary.trim().isNotEmpty,
      effectiveWorkExperiences.isNotEmpty, effectiveEducationEntries.isNotEmpty,
      skillList.isNotEmpty,
    ];
    return ((checks.where((v) => v).length / checks.length) * 100).round();
  }

  ResumeModel copyWith({
    String? fullName, String? targetRole, String? email, String? phone,
    String? location, String? professionalSummary, String? experienceRole,
    String? company, String? experienceDescription, String? degree,
    String? institution, String? educationDetails,
    List<Map<String, String>>? workExperiences,
    List<Map<String, String>>? educationEntries,
    String? skills, String? updatedAt,
  }) => ResumeModel(
    fullName: fullName ?? this.fullName, targetRole: targetRole ?? this.targetRole,
    email: email ?? this.email, phone: phone ?? this.phone,
    location: location ?? this.location,
    professionalSummary: professionalSummary ?? this.professionalSummary,
    experienceRole: experienceRole ?? this.experienceRole,
    company: company ?? this.company,
    experienceDescription: experienceDescription ?? this.experienceDescription,
    degree: degree ?? this.degree, institution: institution ?? this.institution,
    educationDetails: educationDetails ?? this.educationDetails,
    workExperiences: workExperiences ?? this.workExperiences,
    educationEntries: educationEntries ?? this.educationEntries,
    skills: skills ?? this.skills, updatedAt: updatedAt ?? this.updatedAt,
  );

  Map<String, dynamic> toJson() => {
    'fullName': fullName, 'targetRole': targetRole, 'email': email,
    'phone': phone, 'location': location,
    'professionalSummary': professionalSummary,
    'experienceRole': experienceRole, 'company': company,
    'experienceDescription': experienceDescription, 'degree': degree,
    'institution': institution, 'educationDetails': educationDetails,
    'workExperiences': effectiveWorkExperiences,
    'educationEntries': effectiveEducationEntries,
    'skills': skills, 'updatedAt': updatedAt,
  };

  static String _string(Map<String, dynamic> map, String key) =>
      map[key] is String ? map[key] as String : '';

  static List<Map<String, String>> _entries(dynamic value) {
    if (value is! List) return [];
    return value.whereType<Map>().map((item) => item.map(
      (key, value) => MapEntry(key.toString(), value?.toString() ?? ''),
    )).toList();
  }

  factory ResumeModel.fromJson(Map<String, dynamic> json) {
    return ResumeModel(
      fullName: _string(json, 'fullName'), targetRole: _string(json, 'targetRole'),
      email: _string(json, 'email'), phone: _string(json, 'phone'),
      location: _string(json, 'location'),
      professionalSummary: _string(json, 'professionalSummary'),
      experienceRole: _string(json, 'experienceRole'), company: _string(json, 'company'),
      experienceDescription: _string(json, 'experienceDescription'),
      degree: _string(json, 'degree'), institution: _string(json, 'institution'),
      educationDetails: _string(json, 'educationDetails'),
      workExperiences: _entries(json['workExperiences']),
      educationEntries: _entries(json['educationEntries']),
      skills: _string(json, 'skills'), updatedAt: _string(json, 'updatedAt'),
    );
  }

  Map<String, dynamic> toApiJson() => {
    'name': fullName, 'email': email, 'phone': phone, 'location': location,
    'professional_summary': professionalSummary,
    'work_experience': effectiveWorkExperiences.map((e) => {
      'title': e['title'] ?? '', 'company': e['company'] ?? '',
      'description': e['description'] ?? '',
    }).toList(),
    'education': effectiveEducationEntries.map((e) => {
      'degree': e['degree'] ?? '', 'institution': e['institution'] ?? '',
      'description': e['description'] ?? '',
    }).toList(),
    'skills': skillList, 'projects': <Map<String, String>>[],
    'certifications': <String>[], 'industry': targetRole,
    'template_style': 'modern',
  };
}
