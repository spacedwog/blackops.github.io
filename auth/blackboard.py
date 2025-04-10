# auth/blackboard.py
import logging
from auth.auditoria import AuditoriaLogger

logger = logging.getLogger(__name__)

class BlackboardValidator:
    TRUSTED_DOMAINS = {"trusted-domain.com", "partner.org"}

    @staticmethod
    def validar_usuario(user_data, login_input: str) -> bool:
        login = (user_data.get("login") or "").strip().lower()
        email = (user_data.get("email") or "").strip().lower()
        login_input = login_input.strip().lower()

        logger.info(f"🔍 Validando usuário: login_input='{login_input}', login='{login}', email='{email}'")

        if not login_input:
            logger.warning("⚠️ Campo login_input vazio.")
            AuditoriaLogger.registrar_atividade(
                usuario=login or "desconhecido",
                acao="validação de login",
                status="falha",
                detalhes="login_input vazio"
            )
            return False

        if login == login_input:
            logger.info("✅ Login corresponde exatamente ao login_input.")
            AuditoriaLogger.registrar_atividade(
                usuario=login,
                acao="validação de login",
                status="sucesso",
                detalhes="login exato"
            )
            return True

        if "@" in email:
            domain = email.split("@")[1]
            if domain in BlackboardValidator.TRUSTED_DOMAINS:
                logger.info(f"✅ Domínio confiável detectado: {domain}")
                AuditoriaLogger.registrar_atividade(
                    usuario=login,
                    acao="validação de login",
                    status="sucesso",
                    detalhes=f"domínio confiável: {domain}"
                )
                return True
            else:
                logger.warning(f"⚠️ Domínio '{domain}' não é confiável.")

        logger.warning("❌ Validação de usuário falhou.")
        AuditoriaLogger.registrar_atividade(
            usuario=login or "desconhecido",
            acao="validação de login",
            status="falha",
            detalhes="login e domínio não autorizados"
        )
        return False