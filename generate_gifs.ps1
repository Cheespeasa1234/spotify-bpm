# PowerShell script to convert a 133 BPM, 5 s GIF into loops from 60 to 120 BPM (step 5)
$origBPM = 133
$input   = "static/eevee-dance.gif"

for ($bpm = 60; $bpm -le 160; $bpm += 1) {
    # calculate slowdown/speedup factor
    $factor = [math]::Round($origBPM / $bpm, 1)
    $output = "static/dance/${bpm}bpm.gif"

    ffmpeg -y -i $input `
      -filter_complex "[0:v]setpts=${factor}*PTS,split[a][b];[a]palettegen[p];[b][p]paletteuse" `
      $output
}

# Generate the extra one

$bpm = 200

# calculate slowdown/speedup factor
$factor = [math]::Round($origBPM / $bpm, 1)
$output = "static/dance/${bpm}bpm.gif"

ffmpeg -y -i $input `
  -filter_complex "[0:v]setpts=${factor}*PTS,split[a][b];[a]palettegen[p];[b][p]paletteuse" `
  $output