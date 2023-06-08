// Admin Console

// 3 routes - list, add, create using go_router package with a shell route that will render the drawer and app bar

import 'package:champions_admin/champions_admin.dart';

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'constants.dart';

void main() {
  runApp(AdminApp());
}

final _router = GoRouter(
  initialLocation: "/champions",
  routes: [
    ShellRoute(
      builder: (context, state, Widget child) => RootScreen(child: child),
      routes: [
        ChampionsRouter(
            ZenEnvironment.FEDERATION_URL, ZenEnvironment.AUTH_TOKEN),
      ],
    )
  ],
);

class AdminApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      theme: ThemeData(
        primarySwatch: Colors.blue,
        primaryColor: Colors.grey,
        textTheme: const TextTheme(bodyMedium: TextStyle(color: Colors.black)),
      ),
      routerConfig: _router,
    );
  }
}

class RootScreen extends StatelessWidget {
  const RootScreen({
    Key? key,
    required this.child,
  }) : super(key: key);

  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Admin'),
      ),
      drawer: getDrawer(context),
      body: child,
    );
  }
}

Drawer getDrawer(BuildContext context) {
  return Drawer(
    elevation: 0,
    child: ListView(
      padding: EdgeInsets.zero,
      children: [
        const DrawerHeader(
          decoration: BoxDecoration(
            color: Colors.blue,
          ),
          child: Text('Admin'),
        ),
        Container(
          decoration: BoxDecoration(borderRadius: BorderRadius.circular(20)),
          child: ListTile(
            title: const Text('champions'),
            leading: Padding(
              padding: EdgeInsets.all(8),
              child: Icon(
                Icons.event,
                color: Theme.of(context).colorScheme.secondary,
              ),
            ),
            onTap: () {
              context.go('/champions');
            },
          ),
        ),
        ListTile(
          title: const Text('Users'),
          leading: Padding(
            padding: EdgeInsets.all(8),
            child: Icon(
              Icons.supervised_user_circle_rounded,
              color: Theme.of(context).colorScheme.secondary,
            ),
          ),
          onTap: () {
            context.go('/users');
          },
        ),
      ],
    ),
  );
}
