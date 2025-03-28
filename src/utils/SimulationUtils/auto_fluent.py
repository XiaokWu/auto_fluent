import os
import subprocess
import logging
import src.utils.SimulationUtils.fluent_tui as fluent_tui


class AutoFluent:
    
    def __init__(self, simulation_name, mesh_folder_path, case_floder, result_folder, jou_folder, ini_case_folder) -> None:
        self.simulation_name = simulation_name
        self.mesh_folder = mesh_folder_path
        self.case_folder = case_floder
        self.result_folder = result_folder
        self.jou_folder = jou_folder
        self.ini_case_folder = ini_case_folder
        
    def initial (self):
        '''
        生成对应文件夹
        '''
        try:
            os.mkdir(self.simulation_name)
        except(FileExistsError):
            pass
        folders = [self.mesh_folder, self.case_folder, self.jou_folder, self.result_folder]
        for folder in folders:   
            try:
                os.mkdir(os.path.join(self.simulation_name, folder))
            except(FileExistsError):
                pass
    
    @staticmethod
    def clear_folder(folder_path):
        # 确保文件夹存在
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The folder {folder_path} does not exist.")
        
        # 遍历文件夹中的所有文件和子文件夹
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # 如果是文件，删除文件
            if os.path.isfile(file_path):
                os.remove(file_path)
            # 如果是文件夹，递归删除文件夹及其内容
            elif os.path.isdir(file_path):
                os.rmdir(file_path)  # 注意这只会删除空文件夹，如果需要删除非空文件夹，需要使用 shutil.rmtree
                
    def runSimulation(self, flow_variable, case_name, core_num, os_name):
        os.chdir(self.simulation_name)
        os.chdir(self.jou_folder)
        #运行Fluent
        for case in case_name:
            print(f'####################### case_{case} #########################')
            for flow in flow_variable:
                print(f"############# 当前变量：{flow['name']} ################")
                for flow_para in flow['val']:
                    file_name = f"case_{case},{flow['name']}={flow_para}.jou"
                    if os_name == 'Windows':
                        # 构建 Fluent 命令
                        command = f"Fluent 3ddp -t{core_num} -wait -i {file_name}"
                    else:
                        # 构建 Fluent 命令
                        command = f"fluent 3ddp -t{core_num} -wait -i {file_name}"
                    # 执行 Fluent 命令
                    subprocess.run(command, shell=True)
                    print(f"case_{case},{flow['name']}={flow_para} solved")

        print("Fluent 命令执行完毕。")
        os.chdir(os.path.dirname(os.getcwd()))
        self.clear_folder(self.jou_folder)
            
    class Local:
        def __init__(self, autofluent) -> None:
            self.autofluent = autofluent
    
        def joural_gen(self, mesh_name, flow_variable, velocitys):
        # 生成文件
            for mesh in mesh_name:
                meshfile = os.path.join(self.mesh_folder_path,mesh)
                for flow in flow_variable:
                    velocity = velocitys[flow_variable.index(flow)]
                    # 构建文件以及对应保存文件夹
                    file_name = f"mesh_{mesh},flow_variable={flow}.jou"
                    case_name = f'{mesh},{flow}'
                    case_flie_path = os.path.join(self.case_folder,case_name)
                    result_file_case = f"{mesh},{flow}"
                    result_file_path = os.path.join(self.result_folder,result_file_case)
                    jul = f"""
        /file/set-tui-version "23.1"
        /file/set-tui-version "23.1"
        (cx-gui-do cx-activate-item "MenuBar*ReadSubMenu*Mesh...")
        (cx-gui-do cx-set-file-dialog-entries "Select File" '( "{meshfile}.msh.h5") "CFF Mesh Files (*.msh.h5 )")
        (cx-gui-do cx-activate-item "ToolBar*Pointer*translate")
        (cx-gui-do cx-activate-item "General*Table1*ButtonBox1(Mesh)*PushButton4(Units)")
        (cx-gui-do cx-set-list-selections "Set Units*List1(Quantities)" '( 101))
        (cx-gui-do cx-activate-item "Set Units*List1(Quantities)")
        (cx-gui-do cx-set-list-selections "Set Units*Frame3*List1(Units)" '( 1))
        (cx-gui-do cx-activate-item "Set Units*Frame3*List1(Units)")
        (cx-gui-do cx-activate-item "Set Units*PanelButtons*PushButton2(Cancel)")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Models|Energy (Off)"))
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Models|Energy (Off)"))
        (cx-gui-do cx-activate-item "NavigationPane*Frame2*Table1*List_Tree2")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Models|Energy (Off)"))
        (cx-gui-do cx-set-toggle-button2 "Energy*Table1(Energy)*ToggleBox1*CheckButton1(Energy Equation)" #t)
        (cx-gui-do cx-activate-item "Energy*Table1(Energy)*ToggleBox1*CheckButton1(Energy Equation)")
        (cx-gui-do cx-activate-item "Energy*PanelButtons*PushButton1(OK)")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Models|Energy (On)"))
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Materials|Fluid"))
        (cx-gui-do cx-list-tree-right-click "NavigationPane*Frame2*Table1*List_Tree2" )
        (cx-gui-do cx-activate-item "MenuBar*PopupMenuTree-Fluid*New...")
        (cx-gui-do cx-activate-item "Create/Edit Materials*Table1*Frame1*Frame2*ButtonBox2*PushButton1(Fluent Database)")
        (cx-gui-do cx-set-list-selections "Fluent Database Materials*Table1*Frame1*List1(Materials)" '( 1))
        (cx-gui-do cx-activate-item "Fluent Database Materials*Table1*Frame1*List1(Materials)")
        (cx-gui-do cx-set-list-selections "Fluent Database Materials*Table1*Frame1*List1(Materials)" '( 1 565))
        (cx-gui-do cx-activate-item "Fluent Database Materials*Table1*Frame1*List1(Materials)")
        (cx-gui-do cx-activate-item "Fluent Database Materials*PanelButtons*PushButton6(Copy)")
        (cx-gui-do cx-activate-item "Fluent Database Materials*PanelButtons*PushButton1(Close)")
        (cx-gui-do cx-activate-item "Create/Edit Materials*PanelButtons*PushButton1(Close)")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Materials|Solid|aluminum"))
        (cx-gui-do cx-list-tree-right-click "NavigationPane*Frame2*Table1*List_Tree2" )
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Materials|Solid"))
        (cx-gui-do cx-list-tree-right-click "NavigationPane*Frame2*Table1*List_Tree2" )
        (cx-gui-do cx-activate-item "MenuBar*PopupMenuTree-Solid*New...")
        (cx-gui-do cx-activate-item "Create/Edit Materials*Table1*Frame1*Frame2*ButtonBox2*PushButton1(Fluent Database)")
        (cx-gui-do cx-set-list-selections "Fluent Database Materials*Table1*Frame1*Frame3*DropDownList1(Material Type)" '( 1))
        (cx-gui-do cx-activate-item "Fluent Database Materials*Table1*Frame1*Frame3*DropDownList1(Material Type)")
        (cx-gui-do cx-set-list-selections "Fluent Database Materials*Table1*Frame1*List1(Materials)" '( 5))
        (cx-gui-do cx-activate-item "Fluent Database Materials*Table1*Frame1*List1(Materials)")
        (cx-gui-do cx-activate-item "Fluent Database Materials*PanelButtons*PushButton6(Copy)")
        (cx-gui-do cx-activate-item "Fluent Database Materials*PanelButtons*PushButton1(Close)")
        (cx-gui-do cx-activate-item "Create/Edit Materials*PanelButtons*PushButton1(Close)")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Cell Zone Conditions|Fluid|fluid-solid (fluid, id=126)"))
        (cx-gui-do cx-list-tree-right-click "NavigationPane*Frame2*Table1*List_Tree2" )
        (cx-gui-do cx-activate-item "MenuBar*PopupMenuTree-fluid-solid (fluid, id=126)*Edit...")
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 1)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 2)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 2)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 3)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 4)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 5)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 6)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 7)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 8)
        (cx-gui-do cx-activate-tab-index "Fluid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-set-list-selections "Fluid*Frame2*Table1*Table1*DropDownList1(Material Name)" '( 0))
        (cx-gui-do cx-enable-apply-button "Fluid")
        (cx-gui-do cx-activate-item "Fluid*Frame2*Table1*Table1*DropDownList1(Material Name)")
        (cx-gui-do cx-activate-item "Fluid*PanelButtons*PushButton1(OK)")
        (cx-gui-do cx-activate-item "Fluid*PanelButtons*PushButton2(Cancel)")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Cell Zone Conditions|Solid|heatsink-solid (solid, id=123)"))
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Cell Zone Conditions|Solid|heatsink-solid (solid, id=123)"))
        (cx-gui-do cx-list-tree-right-click "NavigationPane*Frame2*Table1*List_Tree2" )
        (cx-gui-do cx-activate-item "MenuBar*PopupMenuTree-heatsink-solid (solid, id=123)*Edit...")
        (cx-gui-do cx-activate-tab-index "Solid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Solid*Frame2*Table3*Frame1" 1)
        (cx-gui-do cx-activate-tab-index "Solid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Solid*Frame2*Table3*Frame1" 2)
        (cx-gui-do cx-activate-tab-index "Solid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Solid*Frame2*Table3*Frame1" 3)
        (cx-gui-do cx-activate-tab-index "Solid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Solid*Frame2*Table3*Frame1" 4)
        (cx-gui-do cx-activate-tab-index "Solid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-activate-tab-index "Solid*Frame2*Table3*Frame1" 5)
        (cx-gui-do cx-activate-tab-index "Solid*Frame2*Table3*Frame1" 0)
        (cx-gui-do cx-set-list-selections "Solid*Frame2*Table1*Table1*DropDownList1(Material Name)" '( 0))
        (cx-gui-do cx-enable-apply-button "Solid")
        (cx-gui-do cx-activate-item "Solid*Frame2*Table1*Table1*DropDownList1(Material Name)")
        (cx-gui-do cx-activate-item "Solid*PanelButtons*PushButton1(OK)")
        (cx-gui-do cx-activate-item "Solid*PanelButtons*PushButton1(OK)")
        (cx-gui-do cx-enable-apply-button "Solid")
        (cx-gui-do cx-activate-item "Solid*PanelButtons*PushButton2(Cancel)")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Boundary Conditions|Inlet"))
        (cx-gui-do cx-list-tree-right-click "NavigationPane*Frame2*Table1*List_Tree2" )
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Boundary Conditions|Inlet|inlet (velocity-inlet, id=28)"))
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Boundary Conditions|Inlet|inlet (velocity-inlet, id=28)"))
        (cx-gui-do cx-list-tree-right-click "NavigationPane*Frame2*Table1*List_Tree2" )
        (cx-gui-do cx-activate-item "MenuBar*PopupMenuTree-inlet (velocity-inlet, id=28)*Edit...")
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 1)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 2)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 3)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 4)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 5)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 6)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 7)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 8)
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
        (cx-gui-do cx-enable-apply-button "Velocity Inlet")
        (cx-gui-do cx-set-expression-entry "Velocity Inlet*Frame2*Frame2*Frame1(Momentum)*Table1*Table9*ExpressionEntry1(Velocity Magnitude)" '("{velocity}" . 0))
        (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 1)
        (cx-gui-do cx-set-expression-entry "Velocity Inlet*Frame2*Frame2*Frame2(Thermal)*Table1*Table1*ExpressionEntry1(Temperature)" '("293.15" . 0))
        (cx-gui-do cx-activate-item "Velocity Inlet*PanelButtons*PushButton1(OK)")
        (cx-gui-do cx-activate-item "Velocity Inlet*PanelButtons*PushButton2(Cancel)")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Boundary Conditions|Wall|heatface (wall, id=30)"))
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Boundary Conditions|Wall|heatface (wall, id=30)"))
        (cx-gui-do cx-list-tree-right-click "NavigationPane*Frame2*Table1*List_Tree2" )
        (cx-gui-do cx-activate-item "MenuBar*PopupMenuTree-heatface (wall, id=30)*Edit...")
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 1)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 2)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 3)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 4)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 5)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 6)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 7)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 8)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 9)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 10)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4*Frame8(Wall Film)*Frame1*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4*Frame8(Wall Film)*Frame1*Frame2" 1)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4*Frame8(Wall Film)*Frame1*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4*Frame8(Wall Film)*Frame1*Frame2" 2)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4*Frame8(Wall Film)*Frame1*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4*Frame8(Wall Film)*Frame1*Frame2" 3)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4*Frame8(Wall Film)*Frame1*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4*Frame8(Wall Film)*Frame1*Frame2" 4)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4*Frame8(Wall Film)*Frame1*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4*Frame8(Wall Film)*Frame1*Frame2" 5)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4*Frame8(Wall Film)*Frame1*Frame2" 0)
        (cx-gui-do cx-activate-tab-index "Wall*Frame4" 1)
        (cx-gui-do cx-enable-apply-button "Wall")
        (cx-gui-do cx-set-expression-entry "Wall*Frame4*Frame2(Thermal)*Frame1*Frame1(Thermal Conditions)*Table3*Table1*Table2*ExpressionEntry1(Heat Flux)" '("1000000" . 0))
        (cx-gui-do cx-activate-item "Wall*PanelButtons*PushButton1(OK)")
        (cx-gui-do cx-activate-item "Wall*PanelButtons*PushButton2(Cancel)")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Methods"))
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Methods"))
        (cx-gui-do cx-activate-item "NavigationPane*Frame2*Table1*List_Tree2")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Methods"))
        (cx-gui-do cx-set-list-selections "Solution Methods*Table1*Table2(Pressure-Velocity Coupling)*DropDownList1(Scheme)" '( 2))
        (cx-gui-do cx-activate-item "Solution Methods*Table1*Table2(Pressure-Velocity Coupling)*DropDownList1(Scheme)")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Initialization"))
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Initialization"))
        (cx-gui-do cx-activate-item "NavigationPane*Frame2*Table1*List_Tree2")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Initialization"))
        (cx-gui-do cx-activate-item "Solution Initialization*Table1*Frame12*PushButton2(Initialize)")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Run Calculation"))
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Run Calculation"))
        (cx-gui-do cx-activate-item "NavigationPane*Frame2*Table1*List_Tree2")
        (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Run Calculation"))
        (cx-gui-do cx-set-integer-entry "Run Calculation*Table1*Table3(Parameters)*Table1*Table1*IntegerEntry1(Number of Iterations)" 300)
        (cx-gui-do cx-activate-item "Run Calculation*Table1*Table3(Parameters)*Table1*Table1*IntegerEntry1(Number of Iterations)")
        (cx-gui-do cx-activate-item "Run Calculation*Table1*Table6(Solution Advancement)*Table1*PushButton1(Calculate)")
        (cx-gui-do cx-activate-item "Information*OK")
        (cx-gui-do cx-activate-item "MenuBar*ExportSubMenu*Solution Data...")
        (cx-gui-do cx-set-list-selections "Export*Table1*Table1*DropDownList2(File Type)" '( 1))
        (cx-gui-do cx-activate-item "Export*Table1*Table1*DropDownList2(File Type)")
        (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table3*List1(Surfaces)" '( 6))
        (cx-gui-do cx-activate-item "Export*Table1*Table2*Table3*List1(Surfaces)")
        (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 34))
        (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
        (cx-gui-do cx-set-toggle-button2 "Export*Table1*Table2*Table1*ToggleBox4(Location)*Cell Center" #t)
        (cx-gui-do cx-activate-item "Export*Table1*Table2*Table1*ToggleBox4(Location)*Cell Center")
        (cx-gui-do cx-activate-item "Export*PanelButtons*PushButton1(OK)")
        (cx-gui-do cx-set-file-dialog-entries "Select File" '( "{result_file_path},out") "ASCII Files ()")
        (cx-gui-do cx-set-list-selections "Export*Table1*Table1*DropDownList2(File Type)" '( 0))
        (cx-gui-do cx-activate-item "Export*Table1*Table1*DropDownList2(File Type)")
        (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table3*List1(Surfaces)" '())
        (cx-gui-do cx-activate-item "Export*Table1*Table2*Table3*List1(Surfaces)")
        (cx-gui-do cx-set-list-selections "Export*Table1*Table1*DropDownList2(File Type)" '( 3))
        (cx-gui-do cx-activate-item "Export*Table1*Table1*DropDownList2(File Type)")
        (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table2*List1(Cell Zones)" '( 1))
        (cx-gui-do cx-activate-item "Export*Table1*Table2*Table2*List1(Cell Zones)")
        (cx-gui-do cx-set-list-selections "Export*Table1*Table1*DropDownList2(File Type)" '( 1))
        (cx-gui-do cx-activate-item "Export*Table1*Table1*DropDownList2(File Type)")
        (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 34))
        (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
        (cx-gui-do cx-activate-item "Export*PanelButtons*PushButton1(OK)")
        (cx-gui-do cx-set-file-dialog-entries "Select File" '( "{result_file_path},sink") "ASCII Files ()")
        (cx-gui-do cx-activate-item "Export*PanelButtons*PushButton2(Cancel)")
        (cx-gui-do cx-activate-item "MenuBar*WriteSubMenu*Case & Data...")
        (cx-gui-do cx-set-file-dialog-entries "Select File" '( "{case_flie_path}.cas.h5") "CFF Case/Data Files (*.cas.h5 *.dat.h5 )")
        /exit y

                """
                
                    file_path = os.path.join(self.jou_folder, file_name)
                    with open(file_path, 'w') as file:
                        file.write(jul)

            print(f"journal文件已生成到 {self.jou_folder} 文件夹中。")
        
        def runSim(self, flow_variable, Mesh_name):
            os.chdir(self.autofluent.jou_folder)
            #运行Fluent
            for mesh in Mesh_name:
                print(f'############# mesh_{mesh} ################')
                for flow in flow_variable:
                    file_name = f"mesh_{mesh},mf={flow}.jou"

                    # 构建 Fluent 命令
                    command = f"Fluent 3ddp -t40 -wait -i {file_name}"

                    # 执行 Fluent 命令
                    subprocess.run(command, shell=True)
                    print(f"mesh_{mesh},massflow={flow} solved")

            print("Fluent 命令执行完毕。")
        

        def joural_gen_case(self, case_name, flow_variable):
            for case in case_name:
                ini_case = os.path.join(self.autofluent.ini_case_folder,case)
                for flow in flow_variable:
                    velocitys = flow['velocity'] 
                    i=0
                    for velocity in velocitys:
                        flow_para = flow['val'][i]
                        # 构建jou文件
                        file_name = f"case_{case},{flow['name']}={flow_para}.jou"
                        case_name = f"case_{case},{flow['name']}={flow_para}"
                        case_flie_path = os.path.join(self.autofluent.simulation_name,self.autofluent.case_folder,case_name)
                        result_file_case = f"case_{case},{flow['name']}={flow_para}"
                        result_file_path = os.path.join(self.autofluent.simulation_name, self.autofluent.result_folder, result_file_case)
                        jul = f"""        
                        /file/set-tui-version "23.1"
            (cx-gui-do cx-activate-item "MenuBar*ReadSubMenu*Case & Data...")
            (cx-gui-do cx-set-file-dialog-entries "Select File" '( "{ini_case}_WATER_2.cas.h5") "CFF Case Files (*.cas.h5 )")
            (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Boundary Conditions|Inlet"))
            (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Setup|Boundary Conditions|Inlet|inlet (velocity-inlet, id=34)"))
            (cx-gui-do cx-list-tree-right-click "NavigationPane*Frame2*Table1*List_Tree2" )
            (cx-gui-do cx-activate-item "MenuBar*PopupMenuTree-inlet (velocity-inlet, id=34)*Edit...")
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 1)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 2)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 3)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 4)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 5)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 6)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 7)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 8)
            (cx-gui-do cx-activate-tab-index "Velocity Inlet*Frame2*Frame2" 0)
            (cx-gui-do cx-enable-apply-button "Velocity Inlet")
            (cx-gui-do cx-set-expression-entry "Velocity Inlet*Frame2*Frame2*Frame1(Momentum)*Table1*Table9*ExpressionEntry1(Velocity Magnitude)" '("{velocity}" . 0))
            (cx-gui-do cx-activate-item "Velocity Inlet*PanelButtons*PushButton1(OK)")
            (cx-gui-do cx-activate-item "Velocity Inlet*PanelButtons*PushButton2(Cancel)")
            (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Initialization"))
            (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Initialization"))
            (cx-gui-do cx-activate-item "NavigationPane*Frame2*Table1*List_Tree2")
            (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Initialization"))
            (cx-gui-do cx-activate-item "Solution Initialization*Table1*Frame9*PushButton1(Initialize)")
            (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Run Calculation"))
            (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Run Calculation"))
            (cx-gui-do cx-activate-item "NavigationPane*Frame2*Table1*List_Tree2")
            (cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Solution|Run Calculation"))
            (cx-gui-do cx-activate-item "Run Calculation*Table1*Table6(Solution Advancement)*Table1*PushButton1(Calculate)")
            (cx-gui-do cx-activate-item "Information*OK")
            (cx-gui-do cx-activate-item "MenuBar*ExportSubMenu*Solution Data...")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table1*DropDownList2(File Type)" '( 1))
            (cx-gui-do cx-activate-item "Export*Table1*Table1*DropDownList2(File Type)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table3*List1(Surfaces)" '( 5))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table3*List1(Surfaces)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table3*List1(Surfaces)" '( 5 6))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table3*List1(Surfaces)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 0))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 0 1))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 0 1 8))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 0 1 8 9))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 0 1 8 9 10))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 0 1 8 9 10 11))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 0 1 8 9 10 11 35))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 0 1 8 9 10 11 35 36))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-activate-item "Export*PanelButtons*PushButton1(OK)")
            (cx-gui-do cx-set-file-dialog-entries "Select File" '( "{result_file_path},surface") "ASCII Files ()")
            (cx-gui-do cx-activate-item "Export*PanelButtons*PushButton1(OK)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table1*DropDownList2(File Type)" '( 1))
            (cx-gui-do cx-activate-item "Export*Table1*Table1*DropDownList2(File Type)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table3*List1(Surfaces)" '( 4 5 6))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table3*List1(Surfaces)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table3*List1(Surfaces)" '( 5 6))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table3*List1(Surfaces)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table3*List1(Surfaces)" '( 6))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table3*List1(Surfaces)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table3*List1(Surfaces)" '())
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table3*List1(Surfaces)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table3*List1(Surfaces)" '( 3))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table3*List1(Surfaces)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 1 8 9 10 11 35 36))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 8 9 10 11 35 36))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 9 10 11 35 36))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 9 11 35 36))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 9 35 36))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-set-list-selections "Export*Table1*Table2*Table4*List1(Quantities)" '( 35 36))
            (cx-gui-do cx-activate-item "Export*Table1*Table2*Table4*List1(Quantities)")
            (cx-gui-do cx-activate-item "Export*PanelButtons*PushButton1(OK)")
            (cx-gui-do cx-set-file-dialog-entries "Select File" '( "{result_file_path},solid") "ASCII Files ()")
            (cx-gui-do cx-activate-item "Export*PanelButtons*PushButton1(OK)")
            (cx-gui-do cx-activate-item "MenuBar*WriteSubMenu*Case & Data...")
            (cx-gui-do cx-set-file-dialog-entries "Select File" '( "{case_flie_path}.cas.h5") "CFF Case/Data Files (*.cas.h5 *.dat.h5 )")
            (cx-gui-do cx-activate-item "MenuBar*FileMenu*Exit")

                        """
                        file_path = os.path.join(self.autofluent.simulation_name, self.autofluent.jou_folder, file_name)
                        with open(file_path, 'w') as file:
                            file.write(jul)
                        print(f"journal文件已生成到 {file_path} 文件夹中。")
                        i+=1
            
        def runSim_case(self, flow_variable, case_name, core_num, os_name, fluent_path = None):
            self.autofluent.runSimulation(flow_variable, case_name, core_num, os_name)

    class Server:
        def __init__(self, autofluent) -> None:
            self.autofluent = autofluent
                  
            
        def joural_gen_beta(self, sim_name, dct_sim_args, dct_result_data, def_path = True):
            file_name = sim_name+'.jou'
            if def_path == True:
                file_path = os.path.join(self.autofluent.simulation_name, self.autofluent.jou_folder, file_name)
                ini_case = os.path.join(self.autofluent.ini_case_folder,f'{dct_sim_args["case"]}.cas.h5').replace('\\', '/')
            else:
                os.mkdir('journal')
                file_path = os.path.join('journal', file_name)
                ini_case = os.path.join(self.autofluent.ini_case_folder.replace('../', ''),f'{dct_sim_args["case"]}.cas.h5').replace('\\', '/')
            dct_sim_args = {**{"ini_case": ini_case}, **dct_sim_args}
            # dct_sim_args = dct_sim_args_new.copy()
            case_file_path = os.path.join(self.autofluent.case_folder,sim_name).replace('\\', '/')
            result_file_case = f"{sim_name}.csv"
            lst_surface = dct_result_data['lst_surface']
            lst_data = dct_result_data['lst_data']
            result_file_path = os.path.join(self.autofluent.result_folder, result_file_case).replace('\\', '/')
            lst_result_args = [result_file_path, lst_surface, lst_data]
            result_dct = {
                    'write_case': case_file_path,
                    'write_result': lst_result_args
            }
            del dct_sim_args['case']
            dct_args = {**dct_sim_args, **result_dct}
            jul = fluent_tui.creat_jou(dct_args)
            self.write_journal(jul, file_path)
            
        def runSim_beta(self, core_num, os_name, fluent_path = None):
            os.chdir(self.autofluent.simulation_name)
            lst_jou = os.listdir(self.autofluent.jou_folder)
            
            for jou_file_name in lst_jou:
                caculated = False
                sim_name = jou_file_name.replace('.jou','')
                for exist_file in os.listdir(self.autofluent.result_folder):
                    if sim_name in exist_file:
                        caculated = True
                        break
                if not caculated:
                    print(f'\n####################################### {sim_name} #######################################')
                    logging.info(f'Running simulation {sim_name}...')
                    jou_path = os.path.join(self.autofluent.jou_folder, jou_file_name)
                    if os_name == 'Windows':
                        # 构建 Fluent 命令
                        command = f"3ddp -g -t{core_num} -i {jou_path}"
                    else:
                        # 构建 Fluent 命令
                        command = f"3ddp -g -t{core_num} -i {jou_path}"
                    #执行 Fluent 命令
                    if fluent_path:
                        os.system(f'{fluent_path} {command}')
                    else:
                        subprocess.run(f'fluent {command}', shell=True)
                    logging.info(f'{sim_name} have been calculated.')
                else:
                    print(f'{sim_name} have been calculated.')
                    
                lst_non_directory_files = [item for item in os.listdir() if os.path.isfile(item)]
                for item in lst_non_directory_files:
                    if 'MPT_Monitor' in item:
                        os.remove(item)
            print("Fluent 命令执行完毕。")
            #self.autofluent.clear_folder(self.autofluent.jou_folder)

        
        def joural_gen_case(self, case_name, flow_variable, dct_sim_para, dct_result_data, path = None):
            for case in case_name:
                ini_case = os.path.join(self.autofluent.ini_case_folder,f'{case}.cas.h5')
                for flow in flow_variable:
                    velocitys = flow['velocity']
                    i=0
                    for velocity in velocitys:
                        flow_para = flow['val'][i]
                        # 构建jou文件
                        file_name = f"case_{case},{flow['name']}={flow_para}.jou"
                        case_name = f"case_{case},{flow['name']}={flow_para}"
                        case_file_path = os.path.join(self.autofluent.case_folder,case_name).replace('\\', '/')
                        result_file_case = f"case_{case},{flow['name']}={flow_para}.csv"
                        result_file_path = os.path.join(self.autofluent.result_folder, result_file_case).replace('\\', '/')
                        lst_heatflux_args = [100000, ['heatface']]
                        lst_velocity_args = [velocity, ['inlet']]
                        lst_surface = dct_result_data['lst_surface']
                        lst_data = dct_result_data['lst_data']
                        lst_result_args = [result_file_path, lst_surface, lst_data]
                        dct_para = {
                            'ini_case': ini_case,
                            'velocity': lst_velocity_args,
                            'heatflux': lst_heatflux_args,
                            'initialize': 'hyb',
                            'iterate': dct_sim_para['iterate'],
                            'write_case': case_file_path,
                            'write_result': lst_result_args
                        }
                        jul = fluent_tui.creat_jou(dct_para)
                        if path == None:
                            file_path = os.path.join(self.autofluent.simulation_name, self.autofluent.jou_folder, file_name)
                        else:
                            file_path = path
                        self.write_journal(jul, file_path)
                        i+=1
                        
        @staticmethod
        def write_journal(journal_content, path):
            with open(path, 'w') as file:
                file.write(journal_content)
            print(f"journal文件已生成到 {path} 文件夹中。")
                        
        def runSim_case(self, flow_variable, case_name, core_num, os_name, fluent_path = None):
            os.chdir(self.autofluent.simulation_name)
            #运行Fluent
            for case in case_name:
                print(f'####################### case_{case} #########################')
                for flow in flow_variable:
                    print(f"############# 当前变量：{flow['name']} ################")
                    for flow_para in flow['val']:
                        file_name = f"case_{case},{flow['name']}={flow_para}.jou"
                        file_name = os.path.join(self.autofluent.jou_folder,file_name)
                        if os_name == 'Windows':
                            # 构建 Fluent 命令
                            command = f"3ddp -g -t{core_num} -i {file_name}"
                        else:
                            # 构建 Fluent 命令
                            command = f"3ddp -g -t{core_num} -i {file_name}"
                        #执行 Fluent 命令
                        if fluent_path:
                            os.system(f'{fluent_path} {command}')
                        else:
                            subprocess.run(f'fluent {command}', shell=True)
                        print(f"case_{case},{flow['name']}={flow_para} solved")
                        lst_non_directory_files = [item for item in os.listdir() if os.path.isfile(item)]
                        for item in lst_non_directory_files:
                            if 'MPT_Monitor' in item:
                                os.remove(item)

            print("Fluent 命令执行完毕。")
            #self.autofluent.clear_folder(self.autofluent.jou_folder)