"""
Signals emitted by the mail feature.
"""

from splent_framework.signals.signal_utils import define_signal

email_sent = define_signal("email-sent", "splent_feature_mail")
