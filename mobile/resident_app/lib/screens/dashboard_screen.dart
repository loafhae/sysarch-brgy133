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
  int _currentIndex = 0;
  
  // State for News Tab
  List<dynamic> _announcements = [];
  bool _isLoadingNews = true;

  // List of screens for the Bottom Bar
  late final List<Widget> _screens;

  @override
  void initState() {
    super.initState();
    
    // Initialize screens
    _screens = [
      NewsTab(
        announcements: _announcements, 
        isLoading: _isLoadingNews,
        refresh: _fetchNews, // Pass function to refresh
      ),
      const FeedbackTab(),
      ProfileTab(fullName: widget.fullName),
    ];

    // Load news immediately when app opens
    _fetchNews();
  }

  // --- FETCH NEWS FUNCTION (Fixed to handle errors) ---
  Future<void> _fetchNews() async {
    setState(() => _isLoadingNews = true);

    try {
      final response = await http.get(Uri.parse('${ApiConstants.baseUrl}/announcements'));
      
      print("Status Code: ${response.statusCode}");
      print("Body: ${response.body}");

      if (response.statusCode == 200) {
        setState(() {
          _announcements = jsonDecode(response.body);
          _isLoadingNews = false;
        });
      } else {
        // Server returned an error (e.g. 500)
        setState(() {
          _announcements = [];
          _isLoadingNews = false;
        });
      }
    } catch (e) {
      // Connection failed (e.g. Server not running)
      print("Connection Error: $e");
      setState(() {
        _announcements = [];
        _isLoadingNews = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Barangay 133"),
        backgroundColor: Colors.red,
      ),
      // Display the screen based on the selected tab
      body: _screens[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
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

// --- TAB 1: NEWS ---
class NewsTab extends StatelessWidget {
  final List<dynamic> announcements;
  final bool isLoading;
  final VoidCallback refresh; // Function to reload data

  const NewsTab({
    super.key, 
    required this.announcements, 
    required this.isLoading,
    required this.refresh
  });

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Center(child: CircularProgressIndicator(color: Colors.red));
    }

    if (announcements.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text("No announcements yet.", style: TextStyle(fontSize: 16)),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: refresh,
              child: const Text("Refresh"),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            )
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: () async => refresh(),
      child: ListView.builder(
        padding: const EdgeInsets.all(10),
        itemCount: announcements.length,
        itemBuilder: (context, index) {
          return Card(
            elevation: 2,
            margin: const EdgeInsets.only(bottom: 10),
            child: ListTile(
              leading: const Icon(Icons.announcement, color: Colors.red),
              title: Text(
                announcements[index]['title'], 
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              subtitle: Text(announcements[index]['body']),
            ),
          );
        },
      ),
    );
  }
}

// --- TAB 2: FEEDBACK ---
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
      final response = await http.post(
        Uri.parse('${ApiConstants.baseUrl}/feedback'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'message': _messageController.text,
          'resident_id': 1, // Dummy ID for testing
        }),
      );
      
      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Feedback Sent!'), backgroundColor: Colors.green),
        );
        _messageController.clear();
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to send'), backgroundColor: Colors.red),
        );
      }
    } catch (e) {
      print(e);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Connection Error'), backgroundColor: Colors.red),
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
            decoration: const InputDecoration(
              labelText: 'Your Message',
              border: OutlineInputBorder(),
              hintText: 'Type your complaint or suggestion here...'
            ),
          ),
          const SizedBox(height: 20),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _submitFeedback,
              style: ElevatedButton.styleFrom(backgroundColor: Colors.red, padding: const EdgeInsets.symmetric(vertical: 15)),