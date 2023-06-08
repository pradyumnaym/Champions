library Champions_admin;

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:go_router/go_router.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'model.dart';

enum ChampionsFormType { EDIT, CREATE }

class ChampionsForm extends StatefulWidget {
  const ChampionsForm({super.key, this.champion, required this.formType});

  final ChampionsData? champion;
  final ChampionsFormType formType;

  @override
  ChampionsFormState createState() => ChampionsFormState();
}

class ChampionsFormState extends State<ChampionsForm> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _nameController;
  late TextEditingController biographyController;
  late TextEditingController _orderController;
  late TextEditingController _linkedinController;
  late TextEditingController _msr_profileController;
  late TextEditingController _avatarController;

  late String _ChampionsMutation;
  late String _label;
  @override
  void initState() {
    print("Form for champion");
    if (widget.formType == ChampionsFormType.EDIT) {
      _nameController = TextEditingController(text: widget.champion!.name);
      biographyController =
          TextEditingController(text: widget.champion!.biography);
      _avatarController = TextEditingController(text: widget.champion!.avatar);
      _orderController =
          TextEditingController(text: widget.champion!.order.toString());
      _linkedinController =
          TextEditingController(text: widget.champion!.linkedin);
      _msr_profileController =
          TextEditingController(text: widget.champion!.msr_profile);

      _ChampionsMutation = '''
              mutation champion(\$champion_id: Int!, \$name: String!, \$biography: String!, \$linkedin: String!, \$msr_profile: String!, \$avatar: String!, \$order: Int!){
                champion(champion_id: \$champion_id, name: \$name, biography: \$biography, linkedin: \$linkedin, msr_profile: \$msr_profile, avatar: \$avatar, order: \$order) {
                  id
                  name
                  biography
                  avatar
                  order
                  linkedin
                  msr_profile
                }
              }
            ''';
      _label = 'Edit Champions ${widget.champion!.id}';
    } else {
      _nameController = TextEditingController();
      biographyController = TextEditingController();
      _avatarController = TextEditingController();
      _orderController = TextEditingController();
      _linkedinController = TextEditingController();
      _msr_profileController = TextEditingController();
      _ChampionsMutation = '''
              mutation champion(\$name: String!, \$biography: String!, \$linkedin: String!, \$msr_profile: String!, \$avatar: String!, \$order: Int!){
                champion(name: \$name, biography: \$biography, linkedin: \$linkedin, msr_profile: \$msr_profile, avatar: \$avatar, order: \$order) {
                  id
                  name
                  biography
                  avatar
                  order
                  linkedin
                  msr_profile
                }
              }
            ''';
      _label = 'Create Champion data';
    }
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: SizedBox(
        width: 500,
        child: Form(
            key: _formKey,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(_label),
                Container(
                  height: 70,
                  width: 700,
                  padding: const EdgeInsets.fromLTRB(10, 0, 10, 0),
                  child: TextFormField(
                    controller: _nameController,
                    decoration: const InputDecoration(
                        labelText: 'name',
                        border: OutlineInputBorder(),
                        focusedBorder: OutlineInputBorder(
                            borderSide: BorderSide(width: 1))),
                    validator: (value) =>
                        value!.isEmpty ? 'name is required' : null,
                  ),
                ),
                Container(
                  height: 70,
                  width: 700,
                  padding: const EdgeInsets.fromLTRB(10, 0, 10, 0),
                  child: TextFormField(
                    controller: biographyController,
                    decoration: const InputDecoration(
                        labelText: 'Data',
                        border: OutlineInputBorder(),
                        focusedBorder: OutlineInputBorder(
                            borderSide: BorderSide(width: 1))),
                  ),
                ),
                Container(
                  height: 70,
                  width: 700,
                  padding: const EdgeInsets.fromLTRB(10, 0, 10, 0),
                  child: TextFormField(
                    controller: _avatarController,
                    decoration: const InputDecoration(
                        labelText: 'Type',
                        border: OutlineInputBorder(),
                        focusedBorder: OutlineInputBorder(
                            borderSide: BorderSide(width: 1))),
                    validator: (value) =>
                        value!.isEmpty ? 'Type is required' : null,
                  ),
                ),
                Padding(padding: EdgeInsets.all(8)),
                Container(
                    height: 70,
                    width: 700,
                    padding: const EdgeInsets.fromLTRB(10, 0, 10, 0),
                    child: TextFormField(
                        controller: _orderController,
                        decoration: const InputDecoration(
                            labelText: 'Order',
                            border: OutlineInputBorder(),
                            focusedBorder: OutlineInputBorder(
                                borderSide: BorderSide(width: 1))))),
                Container(
                  height: 70,
                  width: 700,
                  padding: const EdgeInsets.fromLTRB(10, 0, 10, 0),
                  child: TextFormField(
                    controller: _linkedinController,
                    decoration: const InputDecoration(
                        labelText: 'linkedin',
                        border: OutlineInputBorder(),
                        focusedBorder: OutlineInputBorder(
                            borderSide: BorderSide(width: 1))),
                  ),
                ),
                Container(
                  height: 70,
                  width: 700,
                  padding: const EdgeInsets.fromLTRB(10, 0, 10, 0),
                  child: TextFormField(
                    controller: _msr_profileController,
                    decoration: const InputDecoration(
                        labelText: 'msr_profile',
                        border: OutlineInputBorder(),
                        focusedBorder: OutlineInputBorder(
                            borderSide: BorderSide(width: 1))),
                  ),
                ),
                Mutation(
                    options: MutationOptions(
                      document: gql(_ChampionsMutation),
                      onError: (error) => debugPrint(error.toString()),
                      onCompleted: (data) =>
                          debugPrint("Mutation ran successfully"),
                    ),
                    builder: (RunMutation runMutation, _) {
                      return ElevatedButton(
                        onPressed: () async {
                          if (_formKey.currentState!.validate()) {
                            if (widget.formType == ChampionsFormType.EDIT) {
                              print("edit mutation");
                              print(widget.champion!.id!);
                              await runMutation({
                                "champion_id": widget.champion!.id!,
                                "name": _nameController.text,
                                "biography": biographyController.text,
                                "avatar": _avatarController.text,
                                "order": int.parse(_orderController.text),
                                "linkedin": _linkedinController.text,
                                "msr_profile": _msr_profileController.text
                              }).networkResult;
                            } else {
                              await runMutation({
                                "name": _nameController.text,
                                "biography": biographyController.text,
                                "avatar": _avatarController.text,
                                "order": _orderController == null
                                    ? int.parse(_orderController.text)
                                    : 0,
                                "linkedin": _linkedinController.text,
                                "msr_profile": _msr_profileController.text
                              }).networkResult;
                            }
                            context.pop();
                          }
                        },
                        child: Text('Submit'),
                      );
                    }),
                const Padding(padding: EdgeInsets.all(8)),
                Container(
                  height: 70,
                  padding: const EdgeInsets.all(6),
                  child: ElevatedButton(
                    onPressed: () => context.pop(),
                    child: const Text('Cancel'),
                  ),
                ),
              ],
            )),
      ),
    );
  }
}