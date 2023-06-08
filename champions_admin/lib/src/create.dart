library champions_admin;

import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'champions_form.dart';
import 'package:champions_admin/src/gql_provider.dart';

class ChampionsCreateScreen extends StatelessWidget {
  ChampionsCreateScreen(this.federationUrl, this.authToken) {
    client = GQLProvider(federationUrl, authToken).client;
  }
  String federationUrl, authToken;
  dynamic client;
  @override
  Widget build(BuildContext context) {
    return GraphQLProvider(
        client: client,
        child: const Center(
            child: ChampionsForm(formType: ChampionsFormType.CREATE)));
  }
}
