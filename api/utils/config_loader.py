import yaml

class ConfigLoader:
    """
    ConfigLoader类用于加载和解析配置文件。
    
    参数:
    - config_path (str): 配置文件的路径。
    
    方法:
    - load_config: 加载并返回配置文件的内容。
    """
    def __init__(self, config_path):
        """
        初始化ConfigLoader实例。
        
        参数:
        - config_path (str): 配置文件的路径。
        """
        self.config_path = config_path

    def load_config(self):
        """
        加载配置文件，并以安全方式解析其内容。
        
        返回:
        - dict: 解析后的配置数据。
        """
        with open(self.config_path, "r") as f:  # 打开配置文件
            config = yaml.safe_load(f)  # 安全加载YAML格式的配置数据
        return config