# DragDropTable\n
Customized QTableWidget with more advanced data manipulation capabilities via drag-and-drop interface.\n

The DragDropTable class extends QTableWidget to provide enhanced drag-and-drop functionality within a Qt application. Its primary purpose is to facilitate the rearrangement of table cells through intuitive drag-and-drop operations.\n

Features:\n

Drag-and-Drop Support: The class enables drag-and-drop functionality for cells within the table.\n

Custom Drop Indicator: It features a customizable drop indicator, displayed during drag-and-drop operations, providing visual feedback.\n

Shift and Alt Key Interaction: The class responds to the Shift and Alt keys, allowing to modify the drag-and-drop behavior:\n
\t\t\- no key modifiers - replaces target cell with source cell text and data\n
\t\t\- pressing Shift inserts source cell and it's data to target column\n
\t\t\- pressing Alt - enables copy mode, the source cell will not be cleaned after drop\n
\t\t\- Alt and Shift modifiers can be combined if you need that\n
    
Automatic Cell Cleanup: Optionally, the class can remove empty cells and rows after a drop event, providing a cleaner and more organized table.\n

Use Case:\n
This class is particularly useful in scenarios where users need to rearrange and organize data in a tabular format through an intuitive drag-and-drop interface. It can be applied in various Qt applications, such as those dealing with data management, organization, and manipulation within a table-based user interface.\n
