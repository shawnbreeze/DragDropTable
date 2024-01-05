# DragDropTable
Customized QTableWidget with more advanced data manipulation capabilities via drag-and-drop interface.

The DragDropTable class extends QTableWidget to provide enhanced drag-and-drop functionality within a Qt application. Its primary purpose is to facilitate the rearrangement of table cells through intuitive drag-and-drop operations.

Features:

Drag-and-Drop Support: The class enables drag-and-drop functionality for cells within the table.

Custom Drop Indicator: It features a customizable drop indicator, displayed during drag-and-drop operations, providing visual feedback.

Shift and Alt Key Interaction: The class responds to the Shift and Alt keys, allowing to modify the drag-and-drop behavior:

    - no key modifiers - replaces target cell with source cell text and data
    
    - pressing Shift inserts source cell and it's data to target column
    
    - pressing Alt - enables copy mode, the source cell will not be cleaned after drop
    
    - Alt and Shift modifiers can be combined if you need that
    
    
Automatic Cell Cleanup: Optionally, the class can remove empty cells and rows after a drop event, providing a cleaner and more organized table.

Use Case:
This class is particularly useful in scenarios where users need to rearrange and organize data in a tabular format through an intuitive drag-and-drop interface. It can be applied in various Qt applications, such as those dealing with data management, organization, and manipulation within a table-based user interface.
