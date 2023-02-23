export interface SnackbarMessage {
  show: boolean;
  message: string;
  title: string;
  kind:
    | "error"
    | "info"
    | "info-square"
    | "success"
    | "warning"
    | "warning-alt";
}
