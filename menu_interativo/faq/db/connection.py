"""
Gerenciador de conexão com o banco de dados Oracle.
Implementa o protocolo de contexto para garantir o fechamento da conexão.
"""

import logging

from colorama import Fore, Style

from .schema import check_faq_schema

# Configuração de logging
logger = logging.getLogger(__name__)

# Configuração para a conexão Oracle
_oracle_config = None


def configurar_conexao(config):
    """Configura a conexão global para o banco de dados.

    Args:
        config (dict): Configuração contendo 'user', 'password', 'dsn'
    """
    global _oracle_config
    _oracle_config = config
    logger.info(
        f'{Fore.BLUE}Configuração de conexão Oracle definida com sucesso.{Style.RESET_ALL}'
    )


def obter_conexao(silent=False):
    """Obtém uma nova conexão com o banco de dados usando a configuração global.

    Args:
        silent (bool): Se True, suprime mensagens de log

    Returns:
        OracleConnection: Uma conexão configurada

    Raises:
        ValueError: Se a configuração não tiver sido definida
    """
    if _oracle_config is None:
        error_msg = f'{Fore.RED}Conexão não configurada. Chame configurar_conexao antes.{Style.RESET_ALL}'
        raise ValueError(error_msg)
    return OracleConnection(_oracle_config, silent)


class OracleConnection:
    """Gerencia a conexão com o banco de dados Oracle."""

    def __init__(self, oracle_config, silent=False):
        """Inicializa a conexão com o banco de dados Oracle.

        Args:
            oracle_config (dict): Configuração de conexão ao banco Oracle,
                                 contendo as chaves 'user', 'password' e 'dsn'
            silent (bool): Se True, suprime mensagens de log durante a inicialização

        Raises:
            ImportError: Se o módulo oracledb não estiver instalado
            Exception: Se oracle_config não for fornecido ou se a conexão falhar
        """
        self.conn = None
        self.cursor = None
        self.silent = silent

        try:
            import oracledb

            # Configurando para usar o modo Thin
            # Este modo não requer o Client instalado
            oracledb.defaults.config_dir = None

            if oracle_config:
                self.conn = oracledb.connect(
                    user=oracle_config['user'],
                    password=oracle_config['password'],
                    dsn=oracle_config['dsn'],
                )
                if not silent:
                    print(
                        f'{Fore.BLUE}[INFO] Conexão com o banco de dados Oracle estabelecida (modo Thin).{Style.RESET_ALL}'
                    )
            else:
                error_msg = f'{Fore.RED}oracle_config deve ser fornecido para Oracle{Style.RESET_ALL}'
                raise Exception(error_msg)
            self.cursor = self.conn.cursor()
            # Verifica o schema após estabelecer conexão
            check_faq_schema(self.cursor)
        except ImportError:
            print(
                f'{Fore.RED}oracledb não instalado. Instale com: pip install oracledb{Style.RESET_ALL}'
            )
            raise
        except Exception as e:
            print(
                f'{Fore.RED}[ERRO] Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.{Style.RESET_ALL}'
            )
            print(f'{Fore.RED}Detalhes: {e}{Style.RESET_ALL}')
            raise

    # Implementando o protocolo de contexto para uso com 'with'
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Sempre fecha silenciosamente ao sair do contexto 'with'
        self.close(silent=True)
        return False  # Propaga exceções se houverem

    def close(self, silent=None):
        """Fecha a conexão com o banco de dados de forma segura.

        Args:
            silent (bool, optional): Se True, não exibe mensagens de log ao fechar a conexão.
                                    Se None, usa o valor definido no construtor.
        """
        # Se silent não for explicitamente fornecido, use o valor da instância
        should_be_silent = self.silent if silent is None else silent

        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
        except Exception as e:
            if not should_be_silent:
                logger.warning(
                    f'{Fore.YELLOW}Erro ao fechar o cursor: {e}{Style.RESET_ALL}'
                )

        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                if not should_be_silent:
                    logger.info(
                        f'{Fore.GREEN}Conexão com o banco Oracle fechada com sucesso.{Style.RESET_ALL}'
                    )
        except Exception as e:
            if not should_be_silent:
                logger.warning(
                    f'{Fore.RED}Erro ao fechar a conexão com o banco: {e}{Style.RESET_ALL}'
                )
