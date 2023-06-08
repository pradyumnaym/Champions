library champions_admin;

import 'dart:convert';

class ChampionsData {
  ChampionsData(this.id, this.name, this.biography, this.linkedin, this.order,
      this.msr_profile, this.avatar);

  String? name, biography, linkedin, msr_profile, avatar;
  int? id, order;

  factory ChampionsData.fromJson(Map<String, dynamic> jsonObj) {
    return ChampionsData(
        jsonObj['id'],
        jsonObj['name'] ?? '',
        jsonObj['biography'] ?? '',
        jsonObj['linkedin'] ?? '',
        jsonObj['order'] ?? 0,
        jsonObj['msr_profile'] ?? 0,
        jsonObj['avatar'] ?? '');
  }
}
