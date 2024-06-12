import 'package:flutter/material.dart';

class BakedItemsPage extends StatefulWidget {
  @override
  _BakedItemsPageState createState() => _BakedItemsPageState();
}

class _BakedItemsPageState extends State<BakedItemsPage> {
  List<ItemData> items = [];

  @override
  Widget build(BuildContext context) {
    // Determine the padding based on the screen width
    double screenWidth = MediaQuery.of(context).size.width;
    EdgeInsets padding = screenWidth > 600
        ? EdgeInsets.all(16.0)
        : EdgeInsets.all(8.0);

    return Scaffold(
      appBar: AppBar(
        title: Text('Baked Items'),
      ),
      body: Padding(
        padding: padding,
        child: Column(
          children: [
            ElevatedButton(
              onPressed: () {
                _showAddItemDialog(context);
              },
              child: Text('Add Item'),
            ),
            Expanded(
              child: ListView.builder(
                itemCount: items.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(items[index].name),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        IconButton(
                          icon: Icon(Icons.remove),
                          onPressed: () {
                            setState(() {
                              if (items[index].count > 0) {
                                items[index].count--;
                              }
                            });
                          },
                        ),
                        Text(items[index].count.toString()),
                        IconButton(
                          icon: Icon(Icons.add),
                          onPressed: () {
                            setState(() {
                              items[index].count++;
                            });
                          },
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
            ElevatedButton(
              onPressed: () {
                _submit(context);
              },
              child: Text('Submit'),
            ),
          ],
        ),
      ),
    );
  }

  void _showAddItemDialog(BuildContext context) {
    String newItemName = '';
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Add Item'),
          content: TextField(
            onChanged: (value) {
              newItemName = value;
            },
            decoration: InputDecoration(labelText: 'Item Name'),
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                if (newItemName.isEmpty) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('Please enter item name'),
                      duration: Duration(seconds: 2),
                    ),
                  );
                } else {
                  setState(() {
                    items.add(ItemData(name: newItemName, count: 0));
                  });
                  Navigator.of(context).pop();
                }
              },
              child: Text('Add'),
            ),
          ],
        );
      },
    );
  }

  void _submit(BuildContext context) {
    // Logic to submit data
    Navigator.pop(context); // Navigate back to previous page
  }
}

class ItemData {
  String name;
  int count;

  ItemData({required this.name, required this.count});
}

void main() {
  runApp(MaterialApp(
    home: BakedItemsPage(),
  ));
}
