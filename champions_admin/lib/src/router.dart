import 'package:go_router/go_router.dart';

import 'create.dart';
import 'edit.dart';
import 'list.dart';

GoRoute ChampionsRouter(String FEDERATION_URL, String AUTH_TOKEN) => GoRoute(
      path: '/champions',
      builder: (context, state) => ChampionsScreen(FEDERATION_URL, AUTH_TOKEN),
      routes: [
        GoRoute(
          path: 'edit/:id',
          builder: (context, state) => ChampionsEditScreen(
              FEDERATION_URL, AUTH_TOKEN, int.parse(state.params['id']!)),
        ),
        GoRoute(
          path: 'create',
          builder: (context, state) =>
              ChampionsCreateScreen(FEDERATION_URL, AUTH_TOKEN),
        ),
      ],
    );
