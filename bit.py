from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, random, math, time

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.points = []  # Format: [x, y, dx, dy, x_rank, y_rank]
        self.hexagons1 = []
        self.hexagons2 = []
        self.marked_hexagons1 = []
        self.marked_hexagons2 = set()
        self.NUMBER_OF_POINTS = 200
        self.X_MIN_AREA = 0
        self.Y_MIN_AREA = 0
        self.X_MAX_AREA = 800
        self.Y_MAX_AREA = 800
        self.r = 10
        self.planeSizeText = 800
        self.printPoint = False
        self.printDisk = False
        self.PLANE_OFFSET_X = 300
        self.PLANE_OFFSET_Y = 100

        for _ in range(self.NUMBER_OF_POINTS):
            x = random.randint(self.X_MIN_AREA, self.X_MAX_AREA)
            y = random.randint(self.Y_MIN_AREA, self.Y_MAX_AREA)
            dx = random.uniform(-2, 2)
            dy = random.uniform(-2, 2)
            self.points.append([x, y, dx, dy, -1, -1])

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 1400, 1000)
        self.setWindowTitle('Hexagon & Greedy Solver')
        self.setStyleSheet("background-color: black;")
        self.setupMenu()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_positions)
        #I CHANGED THE TIME NUMBER IT was 50 
        self.timer.start(10)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPlane(qp)
        if self.printPoint:
            self.drawPoints(qp)
        if self.printDisk:
            if str(self.combo.currentText()) == "Hexagon I":
                self.drawHexagon1(qp)
            elif str(self.combo.currentText()) == "Hexagon II":
                self.drawHexagon2(qp)
            elif str(self.combo.currentText()) == "Greedy Max":
                self.greedy_max_algo(qp)
        qp.end()

    def setupMenu(self):
        base_x = 1100
        base_y = 150

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.setStyleSheet("background-color: white; color: black;")
        self.textbox.move(base_x, base_y)
        self.textbox.resize(200, 40)
        self.textbox2 = QtWidgets.QLineEdit(self)
        self.textbox2.setStyleSheet("background-color: white; color: black;")
        self.textbox2.move(base_x, base_y + 65)
        self.textbox2.resize(200, 40)
        self.textbox3 = QtWidgets.QLineEdit(self)
        self.textbox3.setStyleSheet("background-color: white; color: black;")
        self.textbox3.move(base_x, base_y + 210)
        self.textbox3.resize(200, 40)
        self.button = QtWidgets.QPushButton('Create Points', self)
        self.button.setStyleSheet("background-color: white; color: black;")
        self.button.move(base_x, base_y + 130)
        self.button.resize(200, 40)
        self.button.clicked.connect(self.createPoints)
        self.combo = QtWidgets.QComboBox(self)
        self.combo.addItem("Hexagon I")
        self.combo.addItem("Hexagon II")
        self.combo.addItem("Greedy Max")
        self.combo.setStyleSheet("background-color: white; color: black;")
        self.combo.move(base_x, base_y + 275)
        self.combo.resize(200, 25)
        self.button2 = QtWidgets.QPushButton('Find Disks', self)
        self.button2.setStyleSheet("background-color: white; color: black;")
        self.button2.move(base_x, base_y + 325)
        self.button2.resize(200, 40)
        self.button2.clicked.connect(self.findDisks)
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setStyleSheet("background-color: white; color: black;")
        self.textEdit.move(base_x, base_y + 400)
        self.textEdit.resize(200, 150)
        self.textEdit.setReadOnly(True)

    def createPoints(self):
        self.NUMBER_OF_POINTS = int(self.textbox.text())
        self.points = []
        for _ in range(self.NUMBER_OF_POINTS):
            x = random.randint(self.X_MIN_AREA, self.X_MAX_AREA)
            y = random.randint(self.Y_MIN_AREA, self.Y_MAX_AREA)
            dx = random.uniform(-2, 2)
            dy = random.uniform(-2, 2)
            self.points.append([x, y, dx, dy, -1, -1])
        self.printPoint = True
        self.printDisk = False
        self.update()

    def findDisks(self):
        try:
            self.planeSizeText = int(self.textbox2.text())
            self.r = int(self.textbox3.text()) * (800 / self.planeSizeText)
            self.printDisk = True
            self.update()
        except ValueError:
            self.textEdit.setPlainText("Invalid input for Plane Size or Radius!")

    def update_positions(self):
        for point in self.points:
            point[0] += point[2]
            point[1] += point[3]
            if point[0] < self.X_MIN_AREA or point[0] > self.X_MAX_AREA:
                point[2] *= -1
            if point[1] < self.Y_MIN_AREA or point[1] > self.Y_MAX_AREA:
                point[3] *= -1
            point[4] = -1  # x_rank ve y_rank'ı sıfırla
            point[5] = -1
        self.update()

    def drawPlane(self, qp):
        qp.setPen(Qt.white)
        qp.drawRect(self.PLANE_OFFSET_X, self.PLANE_OFFSET_Y, self.X_MAX_AREA, self.Y_MAX_AREA)

    def drawPoints(self, qp):
        qp.setPen(Qt.green)
        for p in self.points:
            qp.drawEllipse(QPointF(p[0] + self.PLANE_OFFSET_X, p[1] + self.PLANE_OFFSET_Y), 2, 2)

    def Regular_Tessellation1(self):
        self.hexagons1 = []
        step_x = self.r * 1.5
        step_y = self.r * math.sqrt(3)
        x_coord = self.r / 2
        while x_coord <= self.X_MAX_AREA:
            row = []
            y_start = self.r / 2 * math.sqrt(3) if len(self.hexagons1) % 2 == 0 else 0
            y_coord = y_start
            while y_coord <= self.Y_MAX_AREA:
                row.append((x_coord, y_coord))
                y_coord += step_y
            self.hexagons1.append(row)
            x_coord += step_x

    def drawHexagon1(self, qp):
        start_time = time.time()
        self.Regular_Tessellation1()
        self.marked_hexagons1 = []
        static_points = [[p[0], p[1], p[4], p[5]] for p in self.points]
        self.Find_hexagons_foreach_point(static_points, self.r, self.hexagons1)
        x_max = len(self.hexagons1)
        y_max = max(len(row) for row in self.hexagons1)
        uncovered_points = static_points.copy()
        x = 0
        while x < x_max - 1:
            y = 0
            while y < y_max - 1:
                comb_list = [(x, y), (x, y+1), (x+1, y), (x+1, y+1)]
                point_list = [p for p in uncovered_points if (p[2], p[3]) in comb_list]
                if point_list:
                    for comb in self.get_combinations(comb_list):
                        covered = [p for p in point_list if self.is_point_covered(p, comb, self.hexagons1)]
                        if len(covered) == len(point_list):
                            self.marked_hexagons1.extend([self.hexagons1[h[0]][h[1]] for h in comb if h[0] < x_max and h[1] < len(self.hexagons1[h[0]])])
                            uncovered_points = [p for p in uncovered_points if p not in covered]
                            break
                y += 2
            x += 2
        # Kapsanmayan noktaları bireysel kapla
        for p in uncovered_points:
            min_dist = float('inf')
            best_hex = None
            for x in range(x_max):
                for y in range(len(self.hexagons1[x])):
                    hex = self.hexagons1[x][y]
                    dist = math.sqrt((p[0] - hex[0])**2 + (p[1] - hex[1])**2)
                    if dist <= self.r and dist < min_dist:
                        min_dist = dist
                        best_hex = hex
            if best_hex:
                self.marked_hexagons1.append(best_hex)
        end_time = time.time()
        duration = end_time - start_time
        stra = f"<<Hexagon I>> {len(self.marked_hexagons1)} disk(s) used to cover {len(self.points)} points\nTime taken: {duration:.3f} seconds"
        self.textEdit.setPlainText(stra)
        qp.setPen(Qt.red)
        for hexagon in self.marked_hexagons1:
            qp.drawEllipse(QPointF(hexagon[0] + self.PLANE_OFFSET_X, hexagon[1] + self.PLANE_OFFSET_Y), self.r, self.r)

    def Regular_Tessellation2(self):
        self.hexagons2 = []
        step_x = self.r * 1.5
        step_y = self.r * math.sqrt(3)
        x_coord = self.r / 2
        while x_coord <= self.X_MAX_AREA:
            row = []
            y_start = self.r / 2 * math.sqrt(3) if len(self.hexagons2) % 2 == 0 else 0
            y_coord = y_start
            while y_coord <= self.Y_MAX_AREA:
                row.append((x_coord, y_coord))
                y_coord += step_y
            self.hexagons2.append(row)
            x_coord += step_x

    def drawHexagon2(self, qp):
        start_time = time.time()
        self.Regular_Tessellation2()
        self.marked_hexagons2 = set()
        uncovered_points = self.points.copy()
        for p in self.points:
            x_rank = int(p[0] / (self.r * 1.5))
            y_rank = int(p[1] / (self.r * math.sqrt(3))) if x_rank % 2 == 0 else int((p[1] + (self.r * math.sqrt(3) / 2)) / (self.r * math.sqrt(3)))
            if x_rank >= len(self.hexagons2) - 1:
                x_rank = len(self.hexagons2) - 2
            if x_rank < 0:
                x_rank = 0
            if y_rank >= len(self.hexagons2[x_rank]) - 1:
                y_rank = len(self.hexagons2[x_rank]) - 2
            if y_rank < 0:
                y_rank = 0

            candidates = [(x_rank, y_rank), (x_rank+1, y_rank)]
            if x_rank % 2 == 0 and y_rank + 1 < len(self.hexagons2[x_rank+1]):
                candidates.append((x_rank+1, y_rank+1))
            elif x_rank % 2 != 0 and y_rank - 1 >= 0:
                candidates.append((x_rank+1, y_rank-1))

            for hex_idx in candidates:
                if hex_idx[0] < len(self.hexagons2) and hex_idx[1] < len(self.hexagons2[hex_idx[0]]):
                    hex = self.hexagons2[hex_idx[0]][hex_idx[1]]
                    if math.sqrt((p[0] - hex[0])**2 + (p[1] - hex[1])**2) <= self.r:
                        self.marked_hexagons2.add(hex)
                        uncovered_points = [up for up in uncovered_points if up != p]
                        break
        # Kapsanmayan noktaları bireysel kapla
        for p in uncovered_points:
            min_dist = float('inf')
            best_hex = None
            for x in range(len(self.hexagons2)):
                for y in range(len(self.hexagons2[x])):
                    hex = self.hexagons2[x][y]
                    dist = math.sqrt((p[0] - hex[0])**2 + (p[1] - hex[1])**2)
                    if dist <= self.r and dist < min_dist:
                        min_dist = dist
                        best_hex = hex
            if best_hex:
                self.marked_hexagons2.add(best_hex)
        end_time = time.time()
        duration = end_time - start_time
        stra = f"<<Hexagon II>> {len(self.marked_hexagons2)} disk(s) used to cover {len(self.points)} points\nTime taken: {duration:.3f} seconds"
        self.textEdit.setPlainText(stra)
        qp.setPen(Qt.blue)
        for hexagon in self.marked_hexagons2:
            qp.drawEllipse(QPointF(hexagon[0] + self.PLANE_OFFSET_X, hexagon[1] + self.PLANE_OFFSET_Y), self.r, self.r)

    
    
    def greedy_max_algo(self, qp):
        start_time = time.time()

        # 1 adım sonrası konumlar
        extrapolated_points = [
            [p[0] + p[2], p[1] + p[3]] for p in self.points
        ]
        disks = []

        while extrapolated_points:
            max_covered = 0
            best_covered_points = []

            # Her nokta merkez alınarak kapsama kontrolü
            for i, pt in enumerate(extrapolated_points):
                x, y = pt
                covered_points = [
                    p for p in extrapolated_points
                    if math.hypot(p[0] - x, p[1] - y) <= self.r
                ]
                if len(covered_points) > max_covered:
                    max_covered = len(covered_points)
                    best_covered_points = covered_points

            # Ağırlık merkezi hesapla ve diski yerleştir
            if best_covered_points:
                x_mean = sum(p[0] for p in best_covered_points) / len(best_covered_points)
                y_mean = sum(p[1] for p in best_covered_points) / len(best_covered_points)
                disks.append((x_mean, y_mean))

                # Bu diskin kapsadığı noktaları listeden çıkar
                extrapolated_points = [
                    p for p in extrapolated_points
                    if math.hypot(p[0] - x_mean, p[1] - y_mean) > self.r
                ]

        # GUI çizimi
        qp.setPen(Qt.yellow)
        for disk in disks:
            qp.drawEllipse(
                QPointF(disk[0] + self.PLANE_OFFSET_X, disk[1] + self.PLANE_OFFSET_Y),
                self.r, self.r
            )

        duration = time.time() - start_time
        stra = f"<<Greedy Max (Extrapolated + Centroid)>> {len(disks)} disk(s) used to cover {len(self.points)} predicted points Time taken: {duration:.3f} seconds"
        self.textEdit.setPlainText(stra)


        # 1 adım sonrası konumlar: x + dx, y + dy
        extrapolated_points = [
            [p[0] + p[2], p[1] + p[3]] for p in self.points
        ]

        disks = []

        while extrapolated_points:
            max_covered = 0
            best_disk_center = None
            best_covered_indices = []

            for i, pt in enumerate(extrapolated_points):
                x, y = pt
                covered_indices = [
                    j for j, p in enumerate(extrapolated_points)
                    if math.sqrt((p[0] - x)**2 + (p[1] - y)**2) <= self.r
                ]
                if len(covered_indices) > max_covered:
                    max_covered = len(covered_indices)
                    best_disk_center = (x, y)
                    best_covered_indices = covered_indices

            if best_disk_center:
                disks.append(best_disk_center)
                extrapolated_points = [
                    p for idx, p in enumerate(extrapolated_points)
                    if idx not in best_covered_indices
                ]

        qp.setPen(Qt.yellow)
        for disk in disks:
            qp.drawEllipse(
                QPointF(disk[0] + self.PLANE_OFFSET_X, disk[1] + self.PLANE_OFFSET_Y),
                self.r, self.r
            )

        duration = time.time() - start_time
        stra = f"<<Greedy Max (Extrapolated)>> {len(disks)} disk(s) used to cover {len(self.points)} predicted points\nTime taken: {duration:.3f} seconds"
        self.textEdit.setPlainText(stra)

        points_to_cover = self.points.copy()
        disks = []
        while points_to_cover:
            max_covered = 0
            best_disk_center = None
            for point in points_to_cover:
                x, y = point[0], point[1]
                covered_points = [
                    p for p in points_to_cover if math.sqrt((p[0] - x) ** 2 + (p[1] - y) ** 2) <= self.r
                ]
                if len(covered_points) > max_covered:
                    max_covered = len(covered_points)
                    best_disk_center = (x, y)
            if best_disk_center:
                disks.append(best_disk_center)
                points_to_cover = [
                    p for p in points_to_cover if math.sqrt((p[0] - best_disk_center[0]) ** 2 + (p[1] - best_disk_center[1]) ** 2) > self.r
                ]
        end_time = time.time()
        duration = end_time - start_time
        qp.setPen(Qt.yellow)
        for disk in disks:
            qp.drawEllipse(QPointF(disk[0] + self.PLANE_OFFSET_X, disk[1] + self.PLANE_OFFSET_Y), self.r, self.r)
        stra = f"<<Greedy Max>> {len(disks)} disk(s) used to cover {len(self.points)} points\nTime taken: {duration:.3f} seconds"
        self.textEdit.setPlainText(stra)

    def Find_hexagons_foreach_point(self, points, r, hexagons):
        for p in points:
            x_rank = int(p[0] / (r * 1.5))
            y_rank = int(p[1] / (r * math.sqrt(3))) if x_rank % 2 == 0 else int((p[1] + (r * math.sqrt(3) / 2)) / (r * math.sqrt(3)))
            if x_rank < len(hexagons) and y_rank < len(hexagons[x_rank]):
                p[2], p[3] = x_rank, y_rank

    def is_point_in_hex_group(self, p, comb_list, hexagons):
        for hex_idx in comb_list:
            if hex_idx[0] < len(hexagons) and hex_idx[1] < len(hexagons[hex_idx[0]]):
                hex = hexagons[hex_idx[0]][hex_idx[1]]
                if math.sqrt((p[0] - hex[0])**2 + (p[1] - hex[1])**2) <= self.r:
                    return True
        return False

    def is_point_covered(self, p, comb, hexagons):
        for hex_idx in comb:
            if hex_idx[0] < len(hexagons) and hex_idx[1] < len(hexagons[hex_idx[0]]):
                hex = hexagons[hex_idx[0]][hex_idx[1]]
                if math.sqrt((p[0] - hex[0])**2 + (p[1] - hex[1])**2) <= self.r:
                    return True
        return False

    def get_combinations(self, comb_list):
        ret = [[]]
        for n in comb_list:
            ret += [r + [n] for r in ret]
        return ret[1:]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
