import 'package:flutter/foundation.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

class GQLProvider {
  GQLProvider(this.federationUrl, this.authToken) {
    httpLink = HttpLink(federationUrl);
    authLink = AuthLink(
      getToken: () async => 'Bearer $authToken',
    );
    client = ValueNotifier<GraphQLClient>(
      GraphQLClient(
        cache: GraphQLCache(),
        link: authLink!.concat(httpLink!),
      ),
    );
  }

  final String federationUrl;
  final String authToken;

  HttpLink? httpLink;
  AuthLink? authLink;
  ValueNotifier<GraphQLClient>? client;
}
