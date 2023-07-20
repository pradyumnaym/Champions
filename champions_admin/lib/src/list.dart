import 'package:champions_admin/src/gql_provider.dart';
import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'model.dart';
import 'package:go_router/go_router.dart';

// Create a list of records from Events from a GraphQL API

class ChampionsScreen extends StatelessWidget {
  ChampionsScreen(this.federationUrl, this.authToken);

  String federationUrl, authToken;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(children: [
          Expanded(
              child: Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              ElevatedButton(
                onPressed: () => context.push("/champions/create"),
                child: Text('+ Create Champions'),
              ),
            ],
          ))
        ]),
        Expanded(child: ChampionsListView(federationUrl, authToken)),
      ],
    );
  }
}

class ChampionsListView extends StatelessWidget {
  ChampionsListView(this.federationUrl, this.authToken) {
    client = GQLProvider(federationUrl, authToken).client;
  }

  String federationUrl, authToken;
  dynamic client;

  @override
  Widget build(BuildContext context) {
    return GraphQLProvider(
      client: client,
      child: Query(
          options: QueryOptions(
            document: gql(r'''

               query {
                champions{
                  id
                  name
                  biography
                  avatar
                  order
                  linkedin
                  msr_profile_id
                  }
                }

            '''),
          ),
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

            final List<ChampionsData> champions = result.data!['champions']
                .map<ChampionsData>((item) => ChampionsData.fromJson(item))
                .toList();

            if (champions.isEmpty) {
              return const Text('No Champions Added');
            } else {
              return SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: DataTable(
                    showCheckboxColumn: false,
                    columns: const [
                      DataColumn(
                        label: Text(
                          "Name",
                        ),
                      ),
                      DataColumn(
                        label: Text("Biography"),
                      ),
                      DataColumn(
                        label: Text(
                          "Linkedin",
                        ),
                      ),
                      DataColumn(
                        label: Text(
                          "MSR Profile",
                        ),
                      ),
                      DataColumn(
                        label: Text(
                          "Avatar",
                        ),
                      ),
                    ],
                    rows: List.generate(
                      champions.length,
                      (index) => championDataRow(context, champions[index]),
                    )),
              );
            }
          }),
    );
  }
}

DataRow championDataRow(BuildContext context, ChampionsData champion) {
  return DataRow(
    onSelectChanged: (value) {
      if (value!) {
        context.push("/champions/edit/${champion.id}");
      }
    },
    cells: [
      DataCell(Text(champion.name!)),
      DataCell(Text(champion.biography!)),
      DataCell(Text(champion.linkedin!)),
      DataCell(Text(champion.msr_profile_id!)),
      DataCell(Text(champion.avatar!))
    ],
  );
}
