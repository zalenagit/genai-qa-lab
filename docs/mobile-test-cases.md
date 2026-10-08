# Mobile app test cases (AI-assisted, reviewed)

Planned test cases for a future mobile version of ZY Demo Store, drafted with AI and reviewed.

| ID | Scenario | Steps | Expected Result | Priority |
| --- | --- | --- | --- | --- |
| MOB-01 | Incoming call during checkout | Fill checkout form, receive a call, return to the app | Form data is kept; no duplicate order | High |
| MOB-02 | Network lost when placing order | Turn on airplane mode, tap Place order | Clear offline message; order is not created twice after reconnecting | High |
| MOB-03 | App sent to background | Add items, switch apps for 5 minutes, return | Cart contents are preserved | Medium |
| MOB-04 | Screen rotation | Rotate on cart and checkout screens | Layout adapts; no data loss | Medium |
| MOB-05 | Session expiry | Leave app idle past the session timeout | User is asked to sign in again; cart is preserved | Medium |
| MOB-06 | Large font / accessibility | Set system font to largest size | All text readable; buttons not cut off | Medium |
| MOB-07 | Push notification deep link | Tap an order notification | Opens that order's details after sign-in | Low |
| MOB-08 | Android crash logs | Reproduce any crash, then run `adb logcat -d \| grep -i "FATAL\|AndroidRuntime"` | Stack trace captured and attached to the bug | High |

**Device matrix (risk-based):** latest iOS and Android, the oldest supported versions, one small-screen phone and one tablet.
