{
  "name": "debug_atul",
  "label": "debug_atul",
  "description": "Runs a user-provided command",
  "version": "1.6",
  "schema-version": "1.0",
  "image": "registry.nrg.wustl.edu/docker/nrg-repo/sharmaatul11/fsl502py369withpacksnltx:latest",
  "type": "docker",
  "command-line": "#COMMAND# > /output/#OUTFILE#",
  "override-entrypoint": true,
  "mounts": [
    {
      "name": "in",
      "writable": false,
      "path": "/input"
    },
    {
      "name": "out",
      "writable": true,
      "path": "/output"
    }
  ],
  "environment-variables": {},
  "ports": {},
  "inputs": [
    {
      "name": "command",
      "description": "The command to run",
      "type": "string",
      "default-value": "echo hello world",
      "required": true,
      "replacement-key": "#COMMAND#",
      "select-values": []
    },
    {
      "name": "output-file",
      "description": "Name of the file to collect stdout",
      "type": "string",
      "default-value": "out.txt",
      "required": false,
      "replacement-key": "#OUTFILE#",
      "select-values": []
    }
  ],
  "outputs": [
    {
      "name": "output",
      "description": "The command's stdout",
      "required": true,
      "mount": "out"
    }
  ],
  "xnat": [
    {
      "name": "debug-project",
      "label": "Debug_atul",
      "description": "Run the debug_atul container with a project mounted",
      "contexts": [
        "xnat:projectData"
      ],
      "external-inputs": [
        {
          "name": "project",
          "description": "Input project",
          "type": "Project",
          "required": true,
          "provides-files-for-command-mount": "in",
          "load-children": false
        }
      ],
      "derived-inputs": [],
      "output-handlers": [
        {
          "name": "output-resource",
          "accepts-command-output": "output",
          "as-a-child-of": "project",
          "type": "Resource",
          "label": "DEBUG_OUTPUT",
          "tags": []
        }
      ]
    },
    {
      "name": "debug-project-asset",
      "label": "Debug_atul",
      "description": "Run the debug_atul container with a project-asset mounted",
      "contexts": [
        "xnat:abstractProjectAsset"
      ],
      "external-inputs": [
        {
          "name": "project-asset",
          "description": "Input project asset",
          "type": "ProjectAsset",
          "required": true,
          "provides-files-for-command-mount": "in",
          "load-children": false
        }
      ],
      "derived-inputs": [],
      "output-handlers": [
        {
          "name": "output-resource",
          "accepts-command-output": "output",
          "as-a-child-of": "project-asset",
          "type": "Resource",
          "label": "DEBUG_OUTPUT",
          "tags": []
        }
      ]
    },
    {
      "name": "debug-subject",
      "description": "Run the debug_atul container with a subject mounted",
      "contexts": [
        "xnat:subjectData"
      ],
      "external-inputs": [
        {
          "name": "subject",
          "description": "Input subject",
          "type": "Subject",
          "required": true,
          "load-children": false
        }
      ],
      "derived-inputs": [],
      "output-handlers": [
        {
          "name": "output-resource",
          "accepts-command-output": "output",
          "as-a-child-of": "subject",
          "type": "Resource",
          "label": "DEBUG_OUTPUT",
          "tags": []
        }
      ]
    },
    {
      "name": "debug-session",
      "label": "Debug_atul",
      "description": "Run the debug_atul container with a session mounted",
      "contexts": [
        "xnat:imageSessionData"
      ],
      "external-inputs": [
        {
          "name": "session",
          "description": "Input session",
          "type": "Session",
          "required": true,
          "provides-files-for-command-mount": "in",
          "load-children": false
        }
      ],
      "derived-inputs": [],
      "output-handlers": [
        {
          "name": "output-resource",
          "accepts-command-output": "output",
          "as-a-child-of": "session",
          "type": "Resource",
          "label": "DEBUG_OUTPUT",
          "tags": []
        }
      ]
    },
    {
      "name": "debug-scan",
      "label": "Debug_atul",
      "description": "Run the debug_atul container with a scan mounted",
      "contexts": [
        "xnat:imageScanData"
      ],
      "external-inputs": [
        {
          "name": "scan",
          "description": "Input scan",
          "type": "Scan",
          "required": true,
          "provides-files-for-command-mount": "in",
          "load-children": false
        }
      ],
      "derived-inputs": [],
      "output-handlers": [
        {
          "name": "output-resource",
          "accepts-command-output": "output",
          "as-a-child-of": "scan",
          "type": "Resource",
          "label": "DEBUG_OUTPUT",
          "tags": []
        }
      ]
    },
    {
      "name": "debug-assessor",
      "label": "Debug_atul",
      "description": "Run the debug_atul container with a assessor mounted",
      "contexts": [
        "xnat:imageAssessorData"
      ],
      "external-inputs": [
        {
          "name": "assessor",
          "description": "Input assessor",
          "type": "Assessor",
          "required": true,
          "provides-files-for-command-mount": "in",
          "load-children": false
        }
      ],
      "derived-inputs": [],
      "output-handlers": [
        {
          "name": "output-resource",
          "accepts-command-output": "output",
          "as-a-child-of": "assessor",
          "type": "Resource",
          "label": "DEBUG_OUTPUT",
          "tags": []
        }
      ]
    }
  ],
  "container-labels": {},
  "generic-resources": {},
  "ulimits": {},
  "secrets": []
}