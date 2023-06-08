library champions_admin;

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:go_router/go_router.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'model.dart';
import 'champions_form.dart';

class ChampionsEditScreen extends StatelessWidget {
  ChampionsEditScreen(this.federationUrl, this.authToken, this.championId);
  String federationUrl, authToken;
  int championId;

  @override
  Widget build(BuildContext context) {
    // fetch the Champions details from GraphQL
    final HttpLink httpLink = HttpLink(federationUrl);

    final AuthLink authLink = AuthLink(
      getToken: () async => 'Bearer $authToken',
    );

    final Link link = authLink.concat(httpLink);

    final ValueNotifier<GraphQLClient> client = ValueNotifier<GraphQLClient>(
      GraphQLClient(
        cache: GraphQLCache(),
        link: link,
      ),
    );

    return GraphQLProvider(
      client: client,
      child: Query(
        options: QueryOptions(document: gql(r'''
              query($championId: Int!){
                champion(id: $championId) {
                  id
                  name
                  biography
                  linkedin
                  msr_profile
                  order
                  avatar
                }
              }
            '''), variables: {'championId': championId}),
        builder: (QueryResult result,
            {VoidCallback? refetch, FetchMore? fetchMore}) {
          if (result.hasException) {
            return Text(result.exception.toString());
          }

          if (result.isLoading) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }

          final ChampionsData champion =
              ChampionsData.fromJson(result.data!['champion']);
          return ChampionsForm(
            champion: champion,
            formType: ChampionsFormType.EDIT,
          );
        },
      ),
    );
  }
}
