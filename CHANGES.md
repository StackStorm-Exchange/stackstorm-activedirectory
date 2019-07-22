# Change Log

## v0.1.4

- Spelling updates in the README.md.
- Removed the incubator installation instructions.

## v0.1.3

- Added automatic change to `http` when using port `5985`.

  Contributed by Nick Maludy (Encore Technologies)
  
- Added catching of JSON parsing errors, so a failure to parse data from JSON
  does not fail the action.
  
  Contributed by Nick Maludy (Encore Technologies)

## v0.1.2

- Fixed `$ProgressPreference=false` by setting it to `$ProgressPreference = 'SilentlyContinue'`

  Contributed by Nick Maludy (Encore Technologies)

## v0.1.1

- In new versions of Powershell if you load a module some text is output into 
  the stream. Pywinrm doesn't handle this gracefully and it leaks into the 
  stderr (https://github.com/diyan/pywinrm/issues/169). This version fixes
  the issue by inserting `$ProgressPreference=false` at the beginning of the
  powershell script that's being run.
  
  Contributed by Brad Bishop (Encore Technologies) #1

## v0.1.0

Initial Revision
