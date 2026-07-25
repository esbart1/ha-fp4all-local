

# ROADMAP

## v01.0
toekomstige versies (automatische omvormernaam, 
instelbare updatefrequentie, realtime-modus voor laden/warmtepomp, enz.).



8. Improve realtime sensors during zero production.

When the inverter is reachable but not producing (night),
report 0 instead of unknown for realtime values such as
Power and Current.

Benefits:
- cleaner history graphs
- simpler Home Assistant automations
- improved EV charging integrations
- no false "unknown" states during nighttime

If the logger itself is unreachable, sensors will still
correctly report unavailable/unknown.