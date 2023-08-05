try:
    import logging
    class SuppressFilter(logging.Filter):
        def filter(self, record):
            return 'wsman' not in record.getMessage()

    from urllib3.connectionpool import log
    log.addFilter(SuppressFilter())
except:
    pass

import winrm
import logging

class RemoteWindowsServer:
    """This class defines a remote windows server connection session. It also provides methods for running windows commands and powershell scripts alongside built-in methods for common tasks.

    Methods
    -------
    - run(cmd:str, capture_error:bool=False)->str: Runs a windows command on the server.
    - powershell(script:str, capture_error:bool=False)->str: Executes a powershell script on the remote server.
    - ping(host:str, packets:int=2)->bool: Pings a host from the server.
    - shut_down(force:bool=False): Shuts down the server.
    - restart(force:bool=False): Restarts the server.
    - manage_services()->RemoteWindowsServer.__ServiceManager: Returns the service manager object for managing services on the server.
    - manage_processes()->RemoteWindowsServer.__ProcessManager: Returns the process manager object for managing processes on the server.
    - bios(*properties:str, **kwargs)->dict: Returns a dictionary with bios data.
    - desktop_settings(*properties, **kwargs)->list: Returns a list of dictionaries with all descktops settings.
    - computer_system(*properties,**kwargs)->dict: Returns a dictionary with information about the computer system.
    - operating_system(*properties, **kwargs)->dict: Returns a dictionary with information about the OS installed.
    - logon_session(*properties, **kwargs)->dict: Returns a dictionary with information about the current logon session.
    - local_time(*properties, **kwargs)->dict: Returns a dictionary with current local time data.
    - processor(*properties, **kwargs)->dict: Returns a dictionary with information about the processor.
    - volumes(*properties, **kwargs)->list: Returns a list of dictionaries with all volumes available or connected to the server.
    - retrieve_data_from_ps_list(stdout:str)->list: Static method that converts standard powershell list to python list of dictionaries.

    Dependencies
    ------------
    - winrm: This class relies on the usage of winrm to connect to remote servers and run commands and powershell scripts on them.
    """

    def __init__(self, host:str, username:str, password:str, port:int=5985, **kwargs):
        logging.info(f'Establishing remote connection with {host}...')
        self.__session = winrm.Session(f"http://{host}:{port}", auth=(username, password),transport=kwargs.get('transport') or 'ntlm',server_cert_validation=kwargs.get('server_cert_validation'),proxy=kwargs.get('proxy'))
        try:
            self.__session.run_cmd("whoami")
            logging.info("Remote connection to the server was successful.")
        except Exception as e:
            logging.critical("Remote connection failed.")
            raise ConnectionError(f"Remote connection to the server at {host} was unsuccessful : {e}" )

        self.__process_manager = self.__ProcessManager(self)
        self.__service_manager = self.__ServiceManager(self)
        pass
 
    def run(self, cmd:str, capture_error:bool=False)->str:
        """Runs a windows command on the server.

        Args
        ----
        - cmd (str): Windows command to be executed.
        - capture_error (bool): False by default, if set to True, standard error will be returned in case of error.

        Returns
        -------
        - str: Standard out or standard error in case of error when capture_error is True.

        Raises
        ------
        - OSError: Raised when the resulted status code is different than 0 and capture_error is False.
        """

        res = self.__session.run_cmd(cmd)
        
        if res.status_code==0:
            return res.std_out.decode().strip()
        elif capture_error:
            return res.std_err.decode().strip()
        else:
            raise OSError(res.std_err.decode().strip())
    
    def powershell(self, script:str, capture_error:bool=False)->str:
        """Executes a powershell script on the server.

        Args
        ----
        - script (str): Powershell script to be executed.
        - capture_error (bool): False by default - if set to True, standard error will be returned in case of error.

        Returns
        -------
        - str: Standard out or standard error in case of error when capture_error is True.

        Raises
        ------
        - OSError: Raised when the resulted status code is different than 0 and capture_error is False.
        """

        res = self.__session.run_ps(script)
        
        if res.status_code==0:
            return res.std_out.decode().strip()
        elif capture_error:
            return res.std_err.decode().strip()
        else:
            raise OSError(res.std_err.decode().strip())
    
    def ping(self, host:str, packets:int=2)->bool:
        """Pings a host from the server.

        Args
        ----
        - host (str): IP address to ping.
        - packets (int): Quantity of packets to send. 2 by default. 

        Returns
        -------
        - bool: False if all packets sent are lost, True otherwise.

        Raises
        ------
        - OSError: Raised when the resulted status code is different than 0.
        """

        output = self.run(f'ping {host} -n {packets}')
        return '100% loss' not in output

    def shut_down(self, force:bool=False):
        """Shuts down the server.

        Args
        ----
        - force (bool): False by default - if set to True, the process will be forced.

        Raises
        ------
        - OSError: Raised when the resulted status code is different than 0.
        """

        forcing = ' -Force' if force else ''
        self.powershell(f'Stop-Computer{forcing}')
        pass

    def restart(self, force:bool=False):
        """Restarts the server.

        Args
        ----
        - force (bool): False by default - if set to True, the process will be forced.

        Raises
        ------
        - OSError: Raised when the resulted status code is different than 0.
        """

        forcing = ' -Force' if force else ''
        self.powershell(f'Restart-Computer{forcing}')
        pass

    def manage_services(self)->'RemoteWindowsServer.__ServiceManager':
        """Returns the service manager object for managing services on the server.

        Returns
        -------
        - RemoteWindowsServer.__ServiceManager: Service manager object.
        """

        return self.__service_manager

    def manage_processes(self)->'RemoteWindowsServer.__ProcessManager':
        """Returns the process manager object for managing processes on the server.

        Returns
        -------
        - RemoteWindowsServer.__ProcessManager: Process manager object.
        """

        return self.__process_manager

    def bios(self, *properties:str, **kwargs)->dict:
        """Returns a dictionary with bios data.

        Args
        ----
        - *properties (str): Argument list of properties to return. Asterisks (*) can be used as wildcards.
        - **kwargs: Arbitrary keyword arguments. 

        Keyword Args
        ------------
        - raw (bool): Used to define whether or not to return the raw standard out instead of the default dictionary.

        Returns
        -------
        - dict: Bios data. The standard out string may be returned instead if raw is found in the keyword arguments and equivalent to True.
            * Status
            * Name
            * Caption
            * SMBIOSPresent
            * Description
            * InstallDate
            * BuildNumber
            * CodeSet
            * IdentificationCode
            * LanguageEdition
            * Manufacturer
            * OtherTargetOS
            * SerialNumber
            * SoftwareElementID
            * SoftwareElementState
            * TargetOperatingSystem
            * Version
            * PrimaryBIOS
            * BiosCharacteristics
            * BIOSVersion
            * CurrentLanguage
            * EmbeddedControllerMajorVersion
            * EmbeddedControllerMinorVersion
            * InstallableLanguages
            * ListOfLanguages
            * ReleaseDate
            * SMBIOSBIOSVersion
            * SMBIOSMajorVersion
            * SMBIOSMinorVersion
            * SystemBiosMajorVersion
            * SystemBiosMinorVersion
            * PSComputerName
            * CimClass
            * CimInstanceProperties
            * CimSystemProperties
        
        Raises
        ------
        - OSError: Raised in case of error.
        """

        raw = kwargs.get('raw')
        data = self.__get_cim_instance('Win32_BIOS', properties, raw)
        return data if raw else data[0]
    
    def desktop_settings(self, *properties, **kwargs)->list:
        """Returns a list of dictionaries with all descktops settings.

        Args
        ----
        - *properties (str): Argument list of properties to return. Asterisks (*) can be used as wildcards.
        - **kwargs: Arbitrary keyword arguments. 

        Keyword Args
        ------------
        - raw (bool): Used to define whether or not to return the raw standard out instead of the default list of dictionaries.

        Returns
        -------
        - list: List of descktops settings. The standard out string may be returned instead if raw is found in the keyword arguments and equivalent to True.
            - dict:
                * Name
                * ScreenSaverActive
                * Caption
                * Description
                * SettingID
                * BorderWidth
                * CoolSwitch
                * CursorBlinkRate
                * DragFullWindows
                * GridGranularity
                * IconSpacing
                * IconTitleFaceName
                * IconTitleSize
                * IconTitleWrap
                * Pattern
                * ScreenSaverExecutable
                * ScreenSaverSecure
                * ScreenSaverTimeout
                * Wallpaper
                * WallpaperStretched
                * WallpaperTiled
                * PSComputerName
                * CimClass
                * CimInstanceProperties
                * CimSystemProperties
        
        Raises
        ------
        - OSError: Raised in case of error.
        """

        return self.__get_cim_instance('Win32_Desktop', properties, kwargs.get('raw'))

    def computer_system(self, *properties,**kwargs)->dict:
        """Returns a dictionary with information about the computer system.

        Args
        ----
        - *properties (str): Argument list of properties to return. Asterisks (*) can be used as wildcards.
        - **kwargs: Arbitrary keyword arguments. 

        Keyword Args
        ------------
        - raw (bool): Used to define whether or not to return the raw standard out instead of the default dictionary.

        Returns
        -------
        - dict: Computer system data. The standard out string may be returned instead if raw is found in the keyword arguments and equivalent to True.
            * AdminPasswordStatus
            * BootupState
            * ChassisBootupState
            * KeyboardPasswordStatus
            * PowerOnPasswordStatus
            * PowerSupplyState
            * PowerState
            * FrontPanelResetStatus
            * ThermalState
            * Status
            * Name
            * PowerManagementCapabilities
            * PowerManagementSupported
            * Caption
            * Description
            * InstallDate
            * CreationClassName
            * NameFormat
            * PrimaryOwnerContact
            * PrimaryOwnerName
            * Roles
            * InitialLoadInfo
            * LastLoadInfo
            * ResetCapability
            * AutomaticManagedPagefile
            * AutomaticResetBootOption
            * AutomaticResetCapability
            * BootOptionOnLimit
            * BootOptionOnWatchDog
            * BootROMSupported
            * BootStatus
            * ChassisSKUNumber
            * CurrentTimeZone
            * DaylightInEffect
            * DNSHostName
            * Domain
            * DomainRole
            * EnableDaylightSavingsTime
            * HypervisorPresent
            * InfraredSupported
            * Manufacturer
            * Model
            * NetworkServerModeEnabled
            * NumberOfLogicalProcessors
            * NumberOfProcessors
            * OEMLogoBitmap
            * OEMStringArray
            * PartOfDomain
            * PauseAfterReset
            * PCSystemType
            * PCSystemTypeEx
            * ResetCount
            * ResetLimit
            * SupportContactDescription
            * SystemFamily
            * SystemSKUNumber
            * SystemStartupDelay
            * SystemStartupOptions
            * SystemStartupSetting
            * SystemType
            * TotalPhysicalMemory
            * UserName
            * WakeUpType
            * Workgroup
            * PSComputerName
            * CimClass
            * CimInstanceProperties
            * CimSystemProperties

        Raises
        ------
        - OSError: Raised in case of error.
        """

        raw = kwargs.get('raw')
        data = self.__get_cim_instance('Win32_ComputerSystem', properties, raw)
        return data if raw else data[0]

    def operating_system(self, *properties, **kwargs)->dict:
        """Returns a dictionary with information about the OS installed.

        Args
        ----
        - *properties (str): Argument list of properties to return. Asterisks (*) can be used as wildcards.
        - **kwargs: Arbitrary keyword arguments. 

        Keyword Args
        ------------
        - raw (bool): Used to define whether or not to return the raw standard out instead of the default dictionary.

        Returns
        -------
        - dict: Operating system data. The standard out string may be returned instead if raw is found in the keyword arguments and equivalent to True.
            * FreePhysicalMemory
            * FreeSpaceInPagingFiles
            * FreeVirtualMemory
            * Caption
            * Description
            * InstallDate
            * CreationClassName
            * CSCreationClassName
            * CSName
            * CurrentTimeZone
            * Distributed
            * LastBootUpTime
            * LocalDateTime
            * MaxNumberOfProcesses
            * MaxProcessMemorySize
            * NumberOfLicensedUsers
            * NumberOfProcesses
            * NumberOfUsers
            * OSType
            * OtherTypeDescription
            * SizeStoredInPagingFiles
            * TotalSwapSpaceSize
            * TotalVirtualMemorySize
            * TotalVisibleMemorySize
            * Version
            * BootDevice
            * BuildNumber
            * BuildType
            * CodeSet
            * CountryCode
            * CSDVersion
            * DataExecutionPrevention_32BitApplications
            * DataExecutionPrevention_Available
            * DataExecutionPrevention_Drivers
            * DataExecutionPrevention_SupportPolicy
            * Debug
            * EncryptionLevel
            * ForegroundApplicationBoost
            * LargeSystemCache
            * Locale
            * Manufacturer
            * MUILanguages
            * OperatingSystemSKU
            * Organization
            * OSArchitecture
            * OSLanguage
            * OSProductSuite
            * PAEEnabled
            * PlusProductID
            * PlusVersionNumber
            * PortableOperatingSystem
            * Primary
            * ProductType
            * RegisteredUser
            * SerialNumber
            * ServicePackMajorVersion
            * ServicePackMinorVersion
            * SuiteMask
            * SystemDevice
            * SystemDirectory
            * SystemDrive
            * WindowsDirectory
            * PSComputerName
            * CimClass
            * CimInstanceProperties
            * CimSystemProperties

        Raises
        ------
        - OSError: Raised in case of error.
        """

        raw = kwargs.get('raw')

        data = self.__get_cim_instance('Win32_OperatingSystem', properties, raw)
        return data if raw else data[0]
    
    def logon_session(self, *properties, **kwargs)->dict:
        """Returns a dictionary with information about the current logon session.

        Args
        ----
        - *properties (str): Argument list of properties to return. Asterisks (*) can be used as wildcards.
        - **kwargs: Arbitrary keyword arguments. 

        Keyword Args
        ------------
        - raw (bool): Used to define whether or not to return the raw standard out instead of the default dictionary.

        Returns
        -------
        - dict: Logon session data. The standard out string may be returned instead if raw is found in the keyword arguments and equivalent to True.
            * Caption
            * Description
            * InstallDate
            * Name
            * Status
            * StartTime
            * AuthenticationPackage
            * LogonId
            * LogonType
            * PSComputerName
            * CimClass
            * CimInstanceProperties
            * CimSystemProperties

        Raises
        ------
        - OSError: Raised in case of error.
        """

        raw = kwargs.get('raw')
        data = self.__get_cim_instance('Win32_LogonSession', properties, raw)
        return data if raw else data[0]
    
    def local_time(self, *properties, **kwargs)->dict:
        """Returns a dictionary with current local time data.

        Args
        ----
        - *properties (str): Argument list of properties to return. Asterisks (*) can be used as wildcards.
        - **kwargs: Arbitrary keyword arguments. 

        Keyword Args
        ------------
        - raw (bool): Used to define whether or not to return the raw standard out instead of the default dictionary.

        Returns
        -------
        - dict: Local time data. The standard out string may be returned instead if raw is found in the keyword arguments and equivalent to True.
            * Day
            * DayOfWeek
            * Hour
            * Milliseconds
            * Minute
            * Month
            * Quarter
            * Second
            * WeekInMonth
            * Year
            * PSComputerName
            * CimClass
            * CimInstanceProperties
            * CimSystemProperties

        Raises
        ------
        - OSError: Raised in case of error.
        """

        raw = kwargs.get('raw')
        data = self.__get_cim_instance('Win32_LocalTime', properties, raw)
        return data if raw else data[0]
    
    def processor(self, *properties, **kwargs)->dict:
        """Returns a dictionary with information about the processor.

        Args
        ----
        - *properties (str): Argument list of properties to return. Asterisks (*) can be used as wildcards.
        - **kwargs: Arbitrary keyword arguments. 

        Keyword Args
        ------------
        - raw (bool): Used to define whether or not to return the raw standard out instead of the default dictionary.

        Returns
        -------
        - dict: Processor data. The standard out string may be returned instead if raw is found in the keyword arguments and equivalent to True.
            * Availability
            * CpuStatus
            * CurrentVoltage
            * DeviceID
            * ErrorCleared
            * ErrorDescription
            * LastErrorCode
            * LoadPercentage
            * Status
            * StatusInfo
            * AddressWidth
            * DataWidth
            * ExtClock
            * L2CacheSize
            * L2CacheSpeed
            * MaxClockSpeed
            * PowerManagementSupported
            * ProcessorType
            * Revision
            * SocketDesignation
            * Version
            * VoltageCaps
            * Caption
            * Description
            * InstallDate
            * Name
            * ConfigManagerErrorCode
            * ConfigManagerUserConfig
            * CreationClassName
            * PNPDeviceID
            * PowerManagementCapabilities
            * SystemCreationClassName
            * SystemName
            * CurrentClockSpeed
            * Family
            * OtherFamilyDescription
            * Role
            * Stepping
            * UniqueId
            * UpgradeMethod
            * Architecture
            * AssetTag
            * Characteristics
            * L3CacheSize
            * L3CacheSpeed
            * Level
            * Manufacturer
            * NumberOfCores
            * NumberOfEnabledCore
            * NumberOfLogicalProcessors
            * PartNumber
            * ProcessorId
            * SecondLevelAddressTranslationExtensions
            * SerialNumber
            * ThreadCount
            * VirtualizationFirmwareEnabled
            * VMMonitorModeExtensions
            * PSComputerName
            * CimClass
            * CimInstanceProperties
            * CimSystemProperties

        Raises
        ------
        - OSError: Raised in case of error.
        """

        raw = kwargs.get('raw')
        data = self.__get_cim_instance('Win32_Processor', properties, raw)
        return data if raw else data[0]
    
    def volumes(self, *properties, **kwargs)->list:
        """Returns a list of dictionaries with all volumes available or connected to the server.

        Args
        ----
        - *properties (str): Argument list of properties to return. Asterisks (*) can be used as wildcards.
        - **kwargs: Arbitrary keyword arguments. 

        Keyword Args
        ------------
        - raw (bool): Used to define whether or not to return the raw standard out instead of the default list of dictionaries.

        Returns
        -------
        - list: List of volumes. The standard out string may be returned instead if raw is found in the keyword arguments and equivalent to True.
            - dict:
                * Status
                * Availability
                * DeviceID
                * StatusInfo
                * Caption
                * Description
                * InstallDate
                * Name
                * ConfigManagerErrorCode
                * ConfigManagerUserConfig
                * CreationClassName
                * ErrorCleared
                * ErrorDescription
                * LastErrorCode
                * PNPDeviceID
                * PowerManagementCapabilities
                * PowerManagementSupported
                * SystemCreationClassName
                * SystemName
                * Access
                * BlockSize
                * ErrorMethodology
                * NumberOfBlocks
                * Purpose
                * FreeSpace
                * Size
                * Compressed
                * DriveType
                * FileSystem
                * MaximumComponentLength
                * MediaType
                * ProviderName
                * QuotasDisabled
                * QuotasIncomplete
                * QuotasRebuilding
                * SupportsDiskQuotas
                * SupportsFileBasedCompression
                * VolumeDirty
                * VolumeName
                * VolumeSerialNumber
                * PSComputerName
                * CimClass
                * CimInstanceProperties
                * CimSystemProperties

        Raises
        ------
        - OSError: Raised in case of error.
        """

        raw = kwargs.get('raw')
        return self.__get_cim_instance('Win32_LogicalDisk', properties, raw)

    def __get_cim_instance(self, name:str, properties:tuple, raw=False)->dict:
        properties = '*' if len(properties)==0 else ' -Property ' + ','.join([f'"{prop}"' for prop in properties])
        stdout = self.powershell(f'Get-CimInstance -ClassName {name} | Format-List {properties}')
        return stdout if raw else self.retrieve_data_from_ps_list(stdout)
    
    def __dict__(self)->dict:
        return self.computer_system(raw=False)
    
    def __str__(self)->str:
        return self.powershell('Systeminfo')

    def __getitem__(self, key):
        return self.computer_system(key, raw=False)[key]

    class __ProcessManager:
        """This class defines the process manager.

        Methods
        -------
        - stop_by_id(*ids, **kwargs): Stops processes by their ids.
        - stop_by_name(*names:str, **kwargs): Stops processes by their names.
        - stop_all_not_responding(force:bool=False): Stops all not-responding processes.
        - start(file_path:str, **kwargs)->str: Starts a process.
        - get_extention_verbs(ext:str)->list: Retrieves a list of verbs available for a given extention.
        - output(*include:str, **kwargs)->str: Outputs a standard powershell table with the processes.
        """

        def __init__(self, server:'RemoteWindowsServer'):
            self.__server = server
            pass

        def stop_by_id(self, *ids, **kwargs):
            """Stops processes by their ids.

            Args
            ----
            - *ids: Argument list of ids.
            - **kwargs: Arbitrary keyword arguments. 

            Keyword Args
            ------------
            - force (bool): Used to define whether or not to force the stopping process(es).

            Raises
            ------
            - OSError: Raised in case of error.
            """

            processes = ','.join([str(id) for id in ids])
            forcing = ' -Force' if kwargs.get('force') else ''
            self.__server.powershell(f'Stop-Process -Id {processes}{forcing}')
            pass

        def stop_by_name(self, *names:str, **kwargs):
            """Stops processes by their names.

            Args
            ----
            - *ids: Argument list of names. Asterisks (*) can be used as wildcards.
            - **kwargs: Arbitrary keyword arguments. 

            Keyword Args
            ------------
            - force (bool): Used to define whether or not to force the stopping process(es).

            Raises
            ------
            - OSError: Raised in case of error.
            """
            
            processes = ','.join([f'"{name}"' for name in names])
            forcing = ' -Force' if kwargs.get('force') else ''
            self.__server.powershell(f'Stop-Process -Name {processes}{forcing}')
            pass
        
        def stop_all_not_responding(self, force:bool=False):
            """Stops all not-responding processes.

            Args
            ----
            - force (bool): Used to define whether or not to force the stopping process(es). Default is False.

            Raises
            ------
            - OSError: Raised in case of error.
            """

            forcing = ' -Force' if force else ''
            self.__server.powershell('Get-Process | Where-Object -FilterScript {$_.Responding -eq $false} | Stop-Process' + forcing)
            pass

        def start(self, file_path:str, **kwargs)->str: 
            """Starts a process.
            Reference: https://docs.microsoft.com/en-us/powershell/module/Microsoft.PowerShell.Management/Start-Process?view=powershell-7.1

            Args
            ----
            - file_path (str): Specifies the path and filename of the program that runs in the process. Enter the name of an executable file or of a document, such as a .txt or .doc file, that is associated with a program on the computer. If you specify only a filename, use the working_directory keyword argument to specify the path.
            - **kwargs: Arbitrary keyword arguments. 

            Keyword Args
            ------------
            - args (list|tuple): Specifies parameters or parameter values to use when this method starts the process
            - working_directory (str): Specifies the location that the new process should start in. The default is the location of the executable file or document being started. Wildcards are not supported. The path name must not contain characters that would be interpreted as wildcards.
            - verb (str): Specifies a verb to use when starting the process. The verbs that are available are determined by the filename extension of the file that runs in the process.
            - redirect_stdin (str): Specifies a file for reading input from it. Enter the path and filename of the input file.
            - redirect_stdout (str): Specifies a file to send the output generated by the process to. Enter the path and filename. By default, the output is returned as a string.
            - redirect_stderr (str): Specifies a file to send any errors generated by the process to. Enter the path and filename. By default, errors are raised.
            - window_style (str): Specifies the state of the window that is used for the new process. The acceptable values for this parameter are: Normal, Hidden, Minimized, and Maximized. The default value is Normal.
            - no_new_window (bool): If True, starts the new process in the current console window. If specified, the window_style param will be ignored.
            - pass_through (bool): Returns, in the standard out, the process object.
            - load_user_profile (bool): Loads the Windows user profile stored in the HKEY_USERS registry key for the current user.
            - wait (bool): If True, waits for the specified process and its descendants to complete before accepting more input. This parameter suppresses the command prompt or retains the window until the processes finish.
            - use_new_environment (bool): If True, uses new environment variables specified for the process. By default, the started process runs with the environment variables inherited from the parent process.

            Returns
            -------
            - str: Standard out. Empty string if the keyword argument pass_through is not found or equivalent to False.

            Raises
            ------
            - OSError: Raised in case of error.
            """

            options = []
            args = kwargs.get('args')
            working_directory = kwargs.get('working_directory')
            verb = kwargs.get('verb')
            redirect_stdin = kwargs.get('redirect_stdin')
            redirect_stdout = kwargs.get('redirect_stdout')
            redirect_stderr = kwargs.get('redirect_stderr')
            window_style = kwargs.get('window_style')

            if args is not None:
                if type(args)==list or type(args)==tuple:
                    args = ','.join([str(arg) for arg in args])
                
                options.append(str(args))
            
            if working_directory is not None:
                options.append(f'-WorkingDirectory "{working_directory}"')
            
            if kwargs.get('load_user_profile'):
                options.append('-LoadUserProfile')
            
            #We either use the NoNewWindow parameter or the WindowStyle one - both cannot be used in the same command.
            if kwargs.get('no_new_window'):
                options.append('-NoNewWindow')
            elif window_style is not None:
                options.append(f'-WindowStyle {window_style}')
                
            if kwargs.get('pass_through'):
                options.append('-PassThru')
            
            if verb is not None:
                options.append(f'-Verb {verb}')
            
            if redirect_stdin is not None:
                options.append(f'-RedirectStandardInput "{redirect_stdin}"')

            if redirect_stdout is not None:
                options.append(f'-RedirectStandardOutput "{redirect_stdout}"')
            
            if redirect_stderr is not None:
                options.append(f'-RedirectStandardError "{redirect_stderr}"')
            
            if kwargs.get('wait'):
                options.append('-Wait')
            
            if kwargs.get('use_new_environment'):
                options.append('-UseNewEnvironment')
            
            options = ' '.join(options)
            return self.__server.powershell(f'Start-Process -FilePath "{file_path}" {options}')

        def get_extention_verbs(self, ext:str)->list:
            """Retrieves a list of verbs available for a given extention.

            Args
            ----
            - ext (str): File extention.

            Returns
            -------
            - list: List of verbs available for the given extention.

            Raises
            ------
            - OSError: Raised in case of error.
            """

            ext = ext if ext[0]=='.' else f'.{ext}'
            stdout = self.__server.powershell(f"""$dg = new-object System.Diagnostics.ProcessStartInfo {ext}
                $dg.verbs""")
            return stdout.split('\n')

        def output(self, *include:str, **kwargs)->str:
            """Outputs a standard powershell table with the processes.
            Default columns are Name and Memory.

            Args
            ----
            - *include: Argument list of properties to include. Asterisks (*) can be used as wildcards. Custom properties will be included between the Name and Memory columns.
            - **kwargs: Arbitrary keyword arguments. 
            
            Keyword Args
            ------------
            - sort (str|list|tuple): Used for specifying a sorting logic. As a string, it must match a property name. As a list or tuple, the first element will define the property name to sort by and the second one will define the order. Consider -1 or 'desc' or 'descending' for descending. Default order is ascending.
            - limit (int): Used for limiting the number of rows for the table.
            - unit (str): Used to specify a unit for the memory column. Default is 'MB'. Accepted values are 'KB', 'MB', 'GB' and 'TB' (case insensitive).

            Returns
            -------
            - str: Standard powershell table.

            Raises
            ------
            - OSError: Raised in case of error.
            """

            sort = kwargs.get('sort')
            limit = kwargs.get('limit') or ''
            memory_unit = kwargs.get('unit')

            sorting = ''
            if sort:
                if type(sort)==str:
                    sort = [sort]
                
                if type(sort)==list or type(sort)==tuple:
                    by = sort[0]
                    if type(by)==tuple:
                        by = list(by)

                    if type(by)!=list:
                        by = [by]

                    for i in range(0, len(by)):
                        if by[i] in ('memory','Memory'):
                            by[i] = 'WS'
                    
                    by = [f'"{att}"' for att in by]
                    by = list(dict.fromkeys(by)) #dedupping
                    by = ','.join(by) #stringifying
                    
                    order = ''
                    if len(sort)>1:
                        str_order = str(sort[1]).upper()
                        if sort[1]==-1 or str_order=='DESC' or str_order=='DESCENDING':
                            order = ' -Descending'
                    sorting = f' | Sort-Object {by}{order}'
            
            if str(limit).isnumeric():
                limit = f' | Select -First {limit}'
            else:
                limit = ''

            unit = str(memory_unit).upper()
            unit = unit if unit in ('TB','GB', 'MB', 'KB') else "MB"

            if len(include)>0:
                include = ',' + ','.join([f'"{prop}"' for prop in include])
            else:
                include = ''

            props = ' "Name"' + include + ',@{l="Memory(' + unit + ')"; e={$_.WS / 1' + unit + '}}'

            return self.__server.powershell('Get-Process' + sorting + limit + ' | ft' + props + ' -AutoSize')

        def __str__(self)->str:
            return self.output(sort=('WS', -1), limit=10)

    class __ServiceManager:
        """This class defines the service manager.

        Methods
        -------
        - get(name:str)->RemoteWindowsServer.__ServiceManager.__Service: Gets a service instance object by its name.
        - has(name:str)->bool: Checks if a service exists.
        - output(*include:str, **kwargs)->str: Outputs a standard powershell table with the services.
        """

        def __init__(self, server:'RemoteWindowsServer'):
            self.__server = server
            pass
        
        def get(self, name:str)->'RemoteWindowsServer.__ServiceManager.__Service':
            """Gets a service instance object by its name.

            Args
            ----
            - name (str): Name of the service to get.
            
            Returns
            -------
            - RemoteWindowsServer.__ServiceManager.__Service: Service instance object.

            Raises
            ------
            - OSError: Raised in case of error.
            """

            self.__server.powershell(f'gsv -Name "{name}"') #This is to verify the service existance.
            return self.__Service(self.__server, name)
        
        def has(self, name:str)->bool:
            """Checks if a service exists.

            Args
            ----
            - name (str): The name of a service.
            
            Returns
            -------
            - bool: True if the service exists, False otherwise.
            """

            try:
                self.__server.powershell(f'gsv -Name "{name}"')
                return True
            except:
                return False

        def output(self, *include:str, **kwargs)->str:
            """Outputs a standard powershell table with the services.
            Default columns are Status, Name and DisplayName.

            Args
            ----
            - *include: Argument list of properties to include. Asterisks (*) can be used as wildcards. Custom properties will be included to the right of DisplayName.
            - **kwargs: Arbitrary keyword arguments. 
            
            Keyword Args
            ------------
            - sort (str|list|tuple): Used for specifying a sorting logic. As a string, it must match a property name. As a list or tuple, the first element will define the property name to sort by and the second one will define the order. Consider -1 or 'desc' or 'descending' for descending. Default order is ascending.
            - limit (int): Used for limiting the number of rows for the table.

            Returns
            -------
            - str: Standard powershell table.

            Raises
            ------
            - OSError: Raised in case of error.
            """

            limit = kwargs.get('limit') or ''
    
            if len(include)>0:
                props = ',' + ','.join([f'"{prop}"' for prop in include])
            else:
                props = ''

            def get_sorting(sort)->str:
                if sort:
                    sort_type = type(sort)
                    if sort_type==str:
                        return f' | Sort-Object "{sort}"'
                    if sort_type==list or sort_type==tuple:
                        by = sort[0]
                        
                        if type(by)==list or type(by)==tuple:
                            by = ','.join([f'"{item}"' for item in by])
                        else:
                            by = f'"{by}"'

                        if len(sort)>1:
                            str_order = str(sort[1]).upper()
                            if sort[1]==-1 or str_order=='DESC' or str_order=='DESCENDING':
                                order = ' -Descending'
                        else:
                            order = ''
                        
                        return f' | Sort-Object {by}{order}'
                        
                return ''
            
            sorting = get_sorting(kwargs.get('sort'))
            
            if str(limit).isnumeric():
                limit = f' | Select -First {limit}'

            return self.__server.powershell('Get-Service' + sorting + limit + ' | ft -Property "Status","Name","DisplayName"' + props + ' -AutoSize')

        class __Service:
            """This class defines a service object.

            Methods
            -------
            - start(): Starts the service.
            - stop(force=False): Stops the service.
            - suspend(): Suspends the service.
            - restart(force=False): Restarts the service.
            - resume(): Resumes the service if paused.
            - get_status()->str: Returns the service current status.
            - get_name()->str: Returns the service name.
            - is_running()->bool: Checks if the service is running.
            - is_stopped()->bool: Checks if the service is stopped.
            - is_paused()->bool: Checks if the service is suspended.
            - requires()->list: Returns a list of service names that is required by this service. 
            - dependents()->list: Returns a list of service names that depends on this service.
            - get_display_name()->str: Returns the service display name.
            - get_service_type()->str: Returns the service type of this service.
            - get_startup_type()->str: Returns the serive startup type.
            - set_startup_type(type:str): Sets the startup type of this service.
            - can_pause_and_continue()->bool: Checks if this service can be paused.
            - can_stop()->bool: Checks if this service can be stopped.
            - can_shut_down()->bool: Checks if this service is notified when the system is shutting down.
            """

            def __init__(self, server:'RemoteWindowsServer', name:str):
                self.__name = name
                self.__server = server
                pass
            
            def start(self):
                """Starts the service.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                
                self.__server.powershell(f'Start-Service -Name {self.__name}')
                pass
            
            def stop(self, force:bool=False):
                """Stops the service.

                Args
                ----
                - force (bool): Used to define whether or not to force the process. Default is False.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                
                forcing = ' -Force' if force else ''
                self.__server.powershell(f'Stop-Service -Name {self.__name}{forcing}')
                pass

            def suspend(self):
                """Suspends the service.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                
                self.__server.powershell(f'Suspend-Service -Name {self.__name}')
                pass

            def restart(self, force:bool=False):
                """Restarts the service.

                Args
                ----
                - force (bool): Used to define whether or not to force the process. Default is False.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                
                forcing = ' -Force' if force else ''
                self.__server.powershell(f'Restart-Service -Name {self.__name}{forcing}')
                pass
            
            def resume(self):
                """Resumes the service.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                
                self.__server.powershell(f'Resume-Service -Name {self.__name}')
                pass
            
            def get_status(self)->str:
                """Returns the service current status.

                Returns
                -------
                - str: Current status.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                
                return self.__get_property_value('Status')
            
            def get_name(self)->str:
                """Returns the service name.

                Returns
                -------
                - str: Service name.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                
                return self.__name
            
            def is_running(self)->bool:
                """Checks if the service is running.

                Returns
                -------
                - bool: True if the service is running, otherwise, False.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                
                return self.get_status()=="Running"
            
            def is_stopped(self)->bool:
                """Checks if the service is stopped.

                Returns
                -------
                - bool: True if the service is stopped, otherwise, False.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                
                return self.get_status()=="Stopped"

            def is_paused(self)->bool:
                """Checks if the service is paused.

                Returns
                -------
                - bool: True if the service is paused, otherwise, False.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                
                return self.get_status()=="Paused"
            
            def requires(self)->list:
                """Returns a list of service names that is required by this service.

                Returns
                -------
                - list: List of service names that is required by this service.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                
                stdout = self.__server.powershell(f'gsv -Name {self.__name} -SDO | Format-Wide -Column 1')
                return [service.strip() for service in stdout.split('\n')]

            def dependents(self)->list:
                """Returns a list of service names that depends on this service.

                Returns
                -------
                - list: List of service names that depends on this service.

                Raises
                ------
                - OSError: Raised in case of error.
                """

                stdout = self.__server.powershell(f'gsv -Name {self.__name} -DS | Format-Wide -Column 1')
                return [service.strip() for service in stdout.split('\n')]

            
            def get_display_name(self)->str:
                """Returns the display name.

                Returns
                -------
                - str: Display name.

                Raises
                ------
                - OSError: Raised in case of error.
                """

                return self.__get_property_value('DisplayName')

            def get_service_type(self)->str:
                """Returns the service type.

                Returns
                -------
                - str: Service type.

                Raises
                ------
                - OSError: Raised in case of error.
                """

                return self.__get_property_value('ServiceType')

            def get_startup_type(self)->str:
                """Returns the startup type.

                Returns
                -------
                - str: Startup type.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                
                return self.__get_property_value('StartType')
            
            def set_startup_type(self, type:str):
                """Sets the Startup Type.

                Args
                ----
                - type (str): Type name.
                    * Boot;
                    * System;
                    * Automatic;
                    * Manual;
                    * Disabled.

                Raises
                ------
                - OSError: Raised in case of error.
                """
                self.__server.powershell(f'Set-Service -Name "{self.__name}" -StartupType {type}')
                pass

            def can_pause_and_continue(self)->bool:
                """Checks if this service can be paused.

                Returns
                ----
                - bool: True if this service can be paused, otherwise, False.

                Raises
                ------
                - OSError: Raised in case of error.
                """

                value = self.__get_property_value('CanPauseAndContinue')
                return value=="True"
            
            def can_stop(self)->bool:
                """Checks if this service can be stopped.

                Returns
                ----
                - bool: True if this service can be stopped, otherwise, False.

                Raises
                ------
                - OSError: Raised in case of error.
                """

                value = self.__get_property_value('CanStop')
                return value=="True"
            
            def can_shut_down(self)->bool:
                """Checks if this service is notified when the system is shutting down.

                Returns
                ----
                - bool: True if this service is notified when the system is shutting down, otherwise, False.

                Raises
                ------
                - OSError: Raised in case of error.
                """

                value = self.__get_property_value('CanShutDown')
                return value=="True"
            
            def __get_property_value(self, property:str)->str:
                return self.__server.powershell(f'gsv -Name {self.__name} | Format-Wide -Property {property}')

            def __dict__(self)->dict:
                stdout = self.__server.powershell(f'gsv -Name "{self.__name}" | Format-List -Property Name,DisplayName,Status,ServiceType,StartType,ServiceName,MachineName,CanPauseAndContinue,CanShutdown,CanStop,ServiceHandle,Site,Container')
                return self.__server.retrieve_data_from_ps_list(stdout)[0]

            def __str__(self)->str:
                return self.__name 

            def __getitem__(self, item):
                if type(item)!=str:
                    return None
                
                value = self.__get_property_value(item)
                return value if value!='' else None
            
            def __eq__(self, other)->bool:
                if type(other)==type(self):
                    return self.get_name() == other.get_name()
                    
                return False

    @staticmethod
    def retrieve_data_from_ps_list(stdout:str)->list:
        """Converts standard powershell list to python list of dictionaries.

        Args
        ----
        stdout (str): Powershell list-formatted standard out.

        Returns
        -------
        list: List of items.
            - dict: Item.
        """

        items = []
        std_items = stdout.replace('\r', '').split('\n\n')
        for item in std_items:
            lines = [line.split(':',1) for line in item.split('\n')]
            data = {}
            for line in lines:
                value = '' if len(line)==1 else line[1].strip()
                
                #pythonizing value
                if value.isnumeric():
                    value = int(value)
                elif value=='True':
                    value = True
                elif value=='False':
                    value = False
                elif value=='None':
                    value = None
                
                data[line[0].strip()] = value
            
            items.append(data) 

        return items
