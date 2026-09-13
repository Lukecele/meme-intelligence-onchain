"""
Alert Engine: Formats and Dispatches High-Priority Intelligence Alerts (Section 5.3)
"""
import logging
import asyncio
import aiohttp
from typing import Dict, Any, List
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from db.database import Database

logger = logging.getLogger(__name__)
console = Console()

class Alerter:
    def __init__(self, db: Database):
        self.db = db

    def format_alert_text(self, signal: Dict[str, Any], risk_flags: List[str]) -> str:
        """
        Formats alert text matching the exact specification in Section 5.3
        """
        symbol = signal.get("symbol", "UNKNOWN")
        mint = signal.get("token_mint", "")
        age_min = signal.get("token_age_minutes", 0)
        mcap = signal.get("market_cap_usd", 0.0)
        liq = signal.get("liquidity_usd", 0.0)
        w_count = signal.get("wallets_count", 0)
        indep_count = signal.get("independent_wallets_count", 0)
        span_min = signal.get("time_span_minutes", 0)
        creator_conc = signal.get("creator_concentration_pct", 0.0)
        level = signal.get("signal_level", "MEDIO")
        
        wallets = signal.get("wallets_involved", [])
        scores_str = ", ".join([f"{w['score']:.0f}/100" for w in wallets[:3]])

        # Cluster breakdown description
        if indep_count == w_count:
            cluster_desc = f"Tutti i {w_count} wallet risultano indipendenti tra loro."
        else:
            clustered_count = w_count - indep_count + 1
            cluster_desc = f"{indep_count - 1} risultano indipendenti, {clustered_count} sono collegati a un cluster storico."

        risks_desc = ", ".join(risk_flags) if risk_flags else "Parametri tecnici regolari, distribuzione monitorata"

        lines = [
            f"🚨 ALERT - anomalia elevata (Intelligence On-Chain)",
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"TOKEN ${symbol} - Solana ({mint[:6]}...{mint[-4:]})",
            f"Età: {age_min:.0f} min | Market cap stimata: ${mcap:,.0f} | Liquidità: ${liq:,.0f}",
            f"{w_count} wallet qualificati sono entrati in {span_min:.0f} minuti. {cluster_desc}",
            f"Wallet score: {scores_str} | Creator concentration: {creator_conc:.1f}%",
            f"Segnale: {level} | Confidenza: {signal.get('confidence', 0.85)*100:.0f}%",
            f"Rischi: {risks_desc}",
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]
        return "\n".join(lines)

    async def dispatch_telegram(self, alert_text: str):
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            return
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": alert_text,
            "parse_mode": "HTML"
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status != 200:
                        logger.warning(f"Telegram alert delivery failed: HTTP {resp.status}")
        except Exception as e:
            logger.error(f"Telegram dispatch error: {e}")

    def render_console_alert(self, alert_text: str, signal_level: str):
        style = "bold green" if signal_level == "ALTO" else "bold yellow"
        panel = Panel(
            Text(alert_text, style="white"),
            title=f"[bold red]⚡ ON-CHAIN CONVERGENCE ALERT [{signal_level}][/bold red]",
            border_style=style,
            expand=False
        )
        console.print(panel)

    async def process_and_dispatch(self, signal: Dict[str, Any], risk_flags: List[str]) -> int:
        alert_text = self.format_alert_text(signal, risk_flags)
        
        # 1. Print to rich terminal console
        self.render_console_alert(alert_text, signal.get("signal_level", "MEDIO"))

        # 2. Save in database alerts table
        alert_id = self.db.insert_alert({
            "token_mint": signal["token_mint"],
            "timestamp": signal["timestamp"],
            "score": signal["score"],
            "confidence": signal["confidence"],
            "signal_level": signal["signal_level"],
            "wallets_count": signal["wallets_count"],
            "independent_wallets_count": signal["independent_wallets_count"],
            "wallets_involved": signal["wallets_involved"],
            "risks_json": risk_flags,
            "market_cap_usd": signal["market_cap_usd"],
            "liquidity_usd": signal["liquidity_usd"],
            "token_age_minutes": signal["token_age_minutes"],
            "alert_text": alert_text,
            "dispatched": 1 if TELEGRAM_BOT_TOKEN else 0
        })

        # 3. Dispatch to Telegram async
        if TELEGRAM_BOT_TOKEN:
            await self.dispatch_telegram(alert_text)

        return alert_id
