import sqlite3
from jinja2 import Template

# Connect to the SQLite database
conn = sqlite3.connect('plant.db')
cursor = conn.cursor()

# Get all plant records
cursor.execute("SELECT * FROM plants")
plants = cursor.fetchall()

# HTML template using Jinja2
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Xeric Garden Tracker</title>
    <style>
        body { font-family: sans-serif; padding: 20px; background: #f5f5f5; }
        table { border-collapse: collapse; width: 100%; background: #fff; }
        th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
        th { background: #4CAF50; color: white; }
        img { max-width: 100px; max-height: 100px; }
    </style>
</head>
<body>
    <h1>🌿 Xeric Garden Tracker</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Code</th>
            <th>Last Watered</th>
            <th>Last Fertilized</th>
            <th>Image</th>
            <th>Notes</th>
        </tr>
        {% for p in plants %}
        <tr>
            <td>{{ p[0] }}</td>
            <td>{{ p[1] }}</td>
            <td>{{ p[2] }}</td>
            <td>{{ p[3] or "–" }}</td>
            <td>{{ p[4] or "–" }}</td>
            <td>
                {% if p[6] %}
                <img src="data:image/jpeg;base64,{{ p[6] }}" />
                {% else %}
                No Image
                {% endif %}
            </td>
            <td>{{ p[5] or "–" }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Render the template
template = Template(html_template)
html_output = template.render(plants=plants)

# Write the output file
with open("plants.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("✅ Exported to plants.html")
