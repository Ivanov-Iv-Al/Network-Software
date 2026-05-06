func CreateTaskHandler(w http.ResponseWriter, r *http.Request) {
    var req struct {
        Title       string `json:"title"`
        Description string `json:"description"`
    }
    json.NewDecoder(r.Body).Decode(&req)

    userID := r.Context().Value("user_id").(string)

    conn, _ := grpc.Dial("task-service:50051", grpc.WithInsecure())
    client := pb.NewTaskServiceClient(conn)
    task, err := client.CreateTask(r.Context(), &pb.CreateTaskRequest{
        UserId:      userID,
        Title:       req.Title,
        Description: req.Description,
    })

    respondJSON(w, 201, task)
}