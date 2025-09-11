"""
Gerenciador de conexão com o banco de dados Oracle.
Implementa o protocolo de contexto para garantir o fechamento da conexão.
"""

import logging

try:
    from colorama import Fore, Style

    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

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
        raise ValueError('Conexão não configurada. Chame configurar_conexao antes.')
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
                    if HAS_COLORAMA:
                        print(
                            f'{Fore.BLUE}[INFO] Conexão com o banco de dados Oracle estabelecida (modo Thin).{Style.RESET_ALL}'
                        )
                    else:
                        print(
                            '[INFO] Conexão com o banco de dados Oracle estabelecida (modo Thin).'
                        )
            else:
                raise Exception('oracle_config deve ser fornecido para Oracle')
            self.cursor = self.conn.cursor()
            # Verifica o schema após estabelecer conexão
            check_faq_schema(self.cursor)
        except ImportError:
            print('oracledb não instalado. Instale com: pip install oracledb')
            raise
        except Exception as e:
            print(
                '[ERRO] Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.'
            )
            print(f'Detalhes: {e}')
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
                logger.warning(f'Erro ao fechar o cursor: {e}')

        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                if not should_be_silent:
                    logger.info('Conexão com o banco Oracle fechada com sucesso.')
        except Exception as e:
            if not should_be_silent:
                logger.warning(f'Erro ao fechar a conexão com o banco: {e}')
