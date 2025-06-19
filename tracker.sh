#!/data/data/com.termux/files/usr/bin/bash

DB="./plant.db"

while true; do
  echo
  echo "🌿 Xeric Garden Plant Tracker"
  echo "----------------------------"
  echo "1. Add Plant"
  echo "2. List Plants"
  echo "3. Update Water/Fertilizer Date"
  echo "4. Add Image to Plant"
  echo "5. Exit"
  echo "----------------------------"
  read -p "Choose an option [1-5]: " option

  case "$option" in
    1)
      read -p "🌱 Plant Name: " name
      read -p "🆔 Plant Code: " code
      sqlite3 "$DB" "INSERT INTO plants (name, code) VALUES ('$name', '$code');"
      echo "✅ Plant '$name' added."
      ;;

    2)
      echo "📋 Plant List"
      sqlite3 -column -header "$DB" "
        SELECT id, name, code, 
               CASE WHEN image_base64 IS NOT NULL THEN '✓' ELSE '×' END AS image,
               last_watered, last_fertilized, notes 
        FROM plants;
      "
      ;;

    3)
      read -p "🔢 Enter Plant ID to update: " pid
      read -p "Update (w)atered or (f)ertilized? " action
      if [[ "$action" == "w" ]]; then
        sqlite3 "$DB" "UPDATE plants SET last_watered = date('now') WHERE id = $pid;"
        echo "💧 Watered date updated."
      elif [[ "$action" == "f" ]]; then
        sqlite3 "$DB" "UPDATE plants SET last_fertilized = date('now') WHERE id = $pid;"
        echo "🌾 Fertilized date updated."
      else
        echo "❌ Invalid option. Use 'w' or 'f'."
      fi
      ;;

    4)
      read -p "🆔 Enter Plant ID to add image: " pid
      read -p "🖼️  Enter image file path (e.g., plant.jpg): " img_path

      if [ ! -f "$img_path" ]; then
        echo "❌ File not found: $img_path"
      else
        echo "🧪 Converting image to base64..."
        img64=$(base64 "$img_path")
        echo "💾 Updating plant ID $pid..."

        echo "UPDATE plants SET image_base64 = '$img64' WHERE id = $pid;" > temp_image.sql
        sqlite3 "$DB" < temp_image.sql
        rm temp_image.sql

        echo "✅ Image saved to database."
      fi
      ;;

    5)
      echo "👋 Exiting... Happy growing!"
      break
      ;;

    *)
      echo "❌ Invalid choice. Please enter 1-5."
      ;;
  esac
done
