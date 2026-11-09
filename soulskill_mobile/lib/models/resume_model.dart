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
    this.projects = const [],
    this.certifications = const [],
    this.skills = '',
    this.updatedAt = '',
  });

  final String fullName, targetRole, email, phone, location, professionalSummary;
  // Legacy fields remain readable so older screens and saved drafts stay compatible.
  final String experienceRole, company, experienceDescription;
  final String degree, institution, educationDetails;
  final List<Map<String, String>> workExperiences;
  final List<Map<String, String>> educationEntries;
  final List<Map<String, String>> projects;
  final List<Map<String, String>> certifications;
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
    List<Map<String, String>>? projects,
    List<Map<String, String>>? certifications,
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
    projects: projects ?? this.projects,
    certifications: certifications ?? this.certifications,
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
    'projects': projects,
    'certifications': certifications,
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

  factory ResumeModel.fromParsedJson(Map<String, dynamic> json) {
    final work = _entries(json['work_entries']).map((entry) => {
      'title': entry['title'] ?? '', 'company': entry['company'] ?? '',
      'description': entry['responsibilities'] ?? entry['description'] ?? '',
      'start_date': entry['start_date'] ?? '', 'end_date': entry['end_date'] ?? '',
    }).toList();
    final education = _entries(json['education_entries']).map((entry) => {
      'degree': entry['degree'] ?? '', 'institution': entry['institution'] ?? '',
      'description': entry['year'] ?? entry['description'] ?? '',
    }).toList();
    final projects = _entries(json['projects']);
    final firstWork = work.isNotEmpty ? work.first : <String, String>{};
    final firstEducation = education.isNotEmpty ? education.first : <String, String>{};
    final rawCertifications = json['certifications'];
    final certificationList = rawCertifications is List
        ? rawCertifications.map((value) => {'name': value.toString(), 'issuer': '', 'date': ''}).toList()
        : (rawCertifications is String && rawCertifications.trim().isNotEmpty
            ? rawCertifications.split(',').map((value) => {'name': value.trim(), 'issuer': '', 'date': ''}).where((value) => value['name']!.isNotEmpty).toList()
            : <Map<String, String>>[]);
    return ResumeModel(
      fullName: _string(json, 'full_name'), email: _string(json, 'email'),
      phone: _string(json, 'phone'), location: _string(json, 'city'),
      professionalSummary: _string(json, 'summary'),
      experienceRole: firstWork['title'] ?? '', company: firstWork['company'] ?? '',
      experienceDescription: firstWork['description'] ?? '',
      degree: firstEducation['degree'] ?? '', institution: firstEducation['institution'] ?? '',
      educationDetails: firstEducation['description'] ?? '',
      workExperiences: work, educationEntries: education,
      certifications: certificationList, projects: projects,
      skills: _string(json, 'tech_skills'),
    );
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
      projects: _entries(json['projects']),
      certifications: _entries(json['certifications']),
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
    'skills': skillList, 'projects': projects,
    'certifications': certifications, 'industry': targetRole,
    'template_style': 'modern',
  };
}
