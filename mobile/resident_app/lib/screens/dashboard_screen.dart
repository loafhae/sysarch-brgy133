import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../constants.dart';

class DashboardScreen extends StatefulWidget {
  final String fullName;

  const DashboardScreen({super.key, required this.fullName});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _currentIndex = 0; // Which tab is open? (0=News, 1=Feedback, 2=Profile)

  // This list holds the 3 screens
  late final List<Widget> _screens;

  @override
  void initState() {
    super.initState();
    // Initialize the screens
    _screens = [
      const NewsTab(),      // Tab 0
      const FeedbackTab(),  // Tab 1
      ProfileTab(fullName: widget.fullName), // Tab 2
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Barangay 133"),
        backgroundColor: Colors.red,
      ),
      // Show the selected screen
      body: _screens[_currentIndex],
      // The Bottom Bar
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index; // Change the tab
          });
        },
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.newspaper), label: 'News'),
          BottomNavigationBarItem(icon: Icon(Icons.feedback), label: 'Feedback'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}

// --- TAB 1: NEWS (Reads from Database) ---
class NewsTab extends StatefulWidget {
  const NewsTab({super.key});

  @override
  State<NewsTab> createState() => _NewsTabState();
}

class _NewsTabState extends State<NewsTab> {
  List<dynamic> _announcements = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchNews(); // Load news when app opens
  }

  Future<void> _fetchNews() async {
    try {
      final response = await http.get(Uri.parse('${ApiConstants.baseUrl}/announcements'));
      if (response.statusCode == 200) {
        setState(() {
          _announcements = jsonDecode(response.body); // Save data
          _isLoading = false;
        });
      }
    } catch (e) {
      print(e);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_announcements.isEmpty) {
      return const Center(child: Text("No announcements yet."));
    }

    return ListView.builder(
      padding: const EdgeInsets.all(10),
      itemCount: _announcements.length,
      itemBuilder: (context, index) {
        return Card(
          child: ListTile(
            leading: const Icon(Icons.announcement, color: Colors.red),
            title: Text(_announcements[index]['title'], style: const TextStyle(fontWeight: FontWeight.bold)),
            subtitle: Text(_announcements[index]['body']),
          ),
        );
      },
    );
  }
}

// --- TAB 2: FEEDBACK (Writes to Database) ---
class FeedbackTab extends StatefulWidget {
  const FeedbackTab({super.key});

  @override
  State<FeedbackTab> createState() => _FeedbackTabState();
}

class _FeedbackTabState extends State<FeedbackTab> {
  final _messageController = TextEditingController();

  Future<void> _submitFeedback() async {
    if (_messageController.text.isEmpty) return;

    try {
      await http.post(
        Uri.parse('${ApiConstants.baseUrl}/feedback'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'message': _messageController.text,
          'resident_id': 1, // Using dummy ID 1 for now
        }),
      );
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Feedback Sent!')),
      );
      _messageController.clear();
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Failed to send')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Column(
        children: [
          TextField(
            controller: _messageController,
            maxLines: 5,
            decoration: const InputDecoration(labelText: 'Your Message', border: OutlineInputBorder()),
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: _submitFeedback,
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text("Send Feedback", style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }
}

// --- TAB 3: PROFILE ---
class ProfileTab extends StatelessWidget {
  final String fullName;
  const ProfileTab({super.key, required this.fullName});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const CircleAvatar(radius: 40, child: Icon(Icons.person, size: 40)),
          const SizedBox(height: 10),
          Text(fullName, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const Text("Resident"),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: () => Navigator.pop(context), // Go back to login
            style: ElevatedButton.styleFrom(backgroundColor: Colors.grey),
            child: const Text("Logout"),
          )
        ],
      ),
    );
  }
}