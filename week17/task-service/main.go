type server struct {
    pb.UnimplementedTaskServiceServer
    db *sql.DB
}

func (s *server) CreateTask(ctx context.Context, req *pb.CreateTaskRequest) (*pb.Task, error) {
	
    if req.Title == "" {
        return nil, status.Error(codes.InvalidArgument, "title required")
    }

    var task pb.Task
    err := s.db.QueryRowContext(ctx,
        "INSERT INTO tasks (user_id, title, description) VALUES ($1, $2, $3) RETURNING id, created_at",
        req.UserId, req.Title, req.Description,
    ).Scan(&task.Id, &task.CreatedAt)
    
    if err != nil {
        return nil, err
    }

    go func() {
        notifyClient.SendNotification(context.Background(), &pb.NotificationRequest{
            UserId: req.UserId,
            Message: "Task created: " + req.Title,
        })
    }()

    task.Title = req.Title
    task.UserId = req.UserId
    task.Status = "pending"
    return &task, nil
}