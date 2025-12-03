foreach ($dir in @("control", "robot_olympics", "test")) {
    python -m mpremote fs mkdir ":$dir" 2>$null
}

Get-ChildItem *.py | ForEach-Object {
    python -m mpremote fs cp $_.Name ":$($_.Name)"
}

foreach ($dir in @("control", "robot_olympics", "test")) {
    Get-ChildItem "$dir\*.py" -ErrorAction SilentlyContinue | ForEach-Object {
        python -m mpremote fs cp $_.FullName ":$dir/$($_.Name)"
    }
}