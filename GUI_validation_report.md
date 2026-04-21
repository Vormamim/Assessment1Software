# GUI Validation Report

## Scope

This document records the validation of the Tkinter GUI in `main.py`, the issues found during testing, and the fixes applied.

## Validation Summary

The GUI was validated in the project virtual environment by:

- launching the application directly with `main.py`
- importing the GUI module with `mainloop()` suppressed to inspect widget creation
- exercising `call_data_search()` programmatically with valid and invalid inputs
- verifying that live API calls still worked through the GUI path

## Results

### Passed checks

- Application startup succeeds in the configured virtual environment.
- The main window and core widgets are created successfully.
- Blank location input shows a warning message.
- Location input containing digits shows an error message.
- Non-numeric magnitude input shows an error message.
- A valid location search for `Sydney` returns earthquake data in the listbox.

### Issues found and fixes

#### 1. GUI startup could fail if `textblob` was missing

Issue:
The application imported `TextBlob` at module load time. If the local environment had not installed that package yet, the GUI crashed before the window opened.

Observed failure:
`ModuleNotFoundError: No module named 'textblob'`

Fix applied:
- `main.py` now treats `TextBlob` as optional.
- Spell checking only runs when `TextBlob` is available.
- This prevents a complete GUI startup failure when the optional spell-check dependency is absent.

Files affected:
- `main.py`

#### 2. The date field default conflicted with the documented GUI behavior

Issue:
The GUI instructions say the date can be left blank if unknown, but `DateEntry` started with a date already populated. That caused searches to be filtered by the current date even when the user had not intentionally chosen one.

Observed behavior:
- Searching for `Sydney` with the default populated date returned `No earthquakes found for this search`.
- Clearing the date field and running the same search returned a valid earthquake result.

Fix applied:
- The `DateEntry` widget is now cleared immediately after creation so the initial GUI state matches the documented behavior.

Files affected:
- `main.py`

#### 3. External API geocoding failed on this Windows environment because of certificate trust

Issue:
The OpenStreetMap geocoding request failed with an SSL certificate verification error on this managed Windows machine.

Observed failure:
`SSLCertVerificationError: self-signed certificate in certificate chain`

Fix applied:
- `earthquakedata.py` now injects the Windows trust store through `truststore` before HTTPS requests are made.
- `requirements.txt` now includes `truststore`.

Result after fix:
- Geocoding for `Sydney` succeeded.
- The earthquake lookup chain completed successfully.

Files affected:
- `earthquakedata.py`
- `requirements.txt`

## Evidence from validation

### Successful positive-path GUI search

Input:
- Location: `Sydney`
- Date: blank
- Magnitude: blank

Observed result:
- Listbox item: `M4.5 - 8 km ENE of Canowindra, Australia`

### Successful validation of error handling

Input:
- Blank location

Observed result:
- Warning shown: `Please add location for a vaild search`

Input:
- Location: `Sydney2`

Observed result:
- Error shown: `You can only put characters in this box`

Input:
- Location: `Sydney`
- Magnitude: `abc`

Observed result:
- Error shown: `You can only put numbers in this section!`

## Remaining notes

- The GUI still contains some spelling mistakes in user-facing messages such as `Invaild` and `vaild`. These do not affect functionality.
- `timezone` is imported in `main.py` but is not used.
- Spell checking is now resilient, but the preferred setup is still to install all dependencies from `requirements.txt`.

## Conclusion

The GUI is functioning after the fixes above. Startup, widget creation, input validation, and live search behavior all passed validation in the current workspace environment.